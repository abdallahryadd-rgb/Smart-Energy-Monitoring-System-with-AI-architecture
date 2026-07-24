using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Ports;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;

namespace AI_Power_Agent
{
    public partial class Form1 : Form
    {
        private SerialPort serialPort;

        // Keeps track of the last exported CSV file path to open it later
        private string lastExportedFile = null;

        // Model for one snapshot/reading
        private class Reading
        {
            public DateTime Time { get; set; }
            public string P1 { get; set; }
            public string P2 { get; set; }
            public string P3 { get; set; }
            public string Raw { get; set; } // optional: raw received line
        }

        // Buffer of all readings to be exported
        private readonly List<Reading> _readings = new List<Reading>();

        public Form1()
        {
            InitializeComponent();
            LoadCOMPorts();

            // Populate baud rate options
            comboBox2.Items.AddRange(new object[] { "9600", "19200", "38400", "57600", "115200" });
            comboBox2.SelectedIndex = 0;

            // Data bits options (not applied below unless you want to use it)
            comboBox3.Items.AddRange(new object[] { "5", "6", "7", "8" });
            comboBox3.SelectedIndex = 3;

            // Disable Disconnect until we are connected
            button2.Enabled = false;

            // Wire up extra buttons
            // button3: Export CSV
            button3.Click += button3_Click;

            // button4: Open last exported CSV
            button4.Click += button4_Click;
        }

        // Designer-linked, do nothing (avoid designer errors)
        private void label1_Click(object sender, EventArgs e)
        {
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Optional init
        }

        private void LoadCOMPorts()
        {
            comboBox1.Items.Clear();
            try
            {
                comboBox1.Items.AddRange(SerialPort.GetPortNames());
            }
            catch
            {
                // Ignore GetPortNames errors
            }

            if (comboBox1.Items.Count > 0) comboBox1.SelectedIndex = 0;
        }

        private void button1_Click(object sender, EventArgs e) // Connect
        {
            try
            {
                if (comboBox1.SelectedItem == null)
                {
                    MessageBox.Show("Select a COM port first.");
                    return;
                }

                // Create and configure the serial port
                serialPort = new SerialPort(
                    comboBox1.SelectedItem.ToString(),
                    int.Parse(comboBox2.SelectedItem.ToString())
                );

                // Optional: apply data bits if you want to use comboBox3 value
                // serialPort.DataBits = int.Parse(comboBox3.SelectedItem.ToString());

                serialPort.NewLine = "\n";                  // ReadLine ends at '\n'
                serialPort.Encoding = Encoding.ASCII;       // ASCII is typical for microcontrollers
                serialPort.ReadTimeout = 800;               // Avoid infinite blocking on ReadLine
                serialPort.DtrEnable = false;               // If Arduino resets on open, try true
                serialPort.RtsEnable = false;

                serialPort.DataReceived += SerialPort_DataReceived;
                serialPort.Open();

                progressBar1.Value = 100;
                button1.Enabled = false; // disable Connect
                button2.Enabled = true;  // enable Disconnect

                richTextBox1.AppendText($"[Opened {serialPort.PortName} @ {serialPort.BaudRate}]{Environment.NewLine}");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Open error: " + ex.Message);
            }
        }

        private void button2_Click(object sender, EventArgs e) // Disconnect
        {
            try
            {
                if (serialPort != null)
                {
                    if (serialPort.IsOpen)
                    {
                        serialPort.DataReceived -= SerialPort_DataReceived;
                        serialPort.Close();
                    }

                    serialPort.Dispose();
                    serialPort = null;
                }

                button1.Enabled = true;  // enable Connect
                button2.Enabled = false; // disable Disconnect

                richTextBox1.AppendText("[Closed]" + Environment.NewLine);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Close error: " + ex.Message);
            }
        }

        private void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            try
            {
                if (serialPort == null || !serialPort.IsOpen)
                    return;

                string line = null;

                try
                {
                    // Preferred: read a full line
                    line = serialPort.ReadLine();
                }
                catch (TimeoutException)
                {
                    // Fallback: read whatever is available
                    try { line = serialPort.ReadExisting(); }
                    catch { line = null; }
                }

                if (string.IsNullOrEmpty(line))
                    return;

                // Marshal UI updates to UI thread
                this.BeginInvoke(new Action(() =>
                {
                    richTextBox1.AppendText(line + Environment.NewLine);
                    ParseSimple(line);
                }));
            }
            catch (Exception ex)
            {
                // If form is closing, this may fail—ignore safely
                try
                {
                    this.BeginInvoke(new Action(() =>
                        richTextBox1.AppendText("[RecvErr] " + ex.Message + Environment.NewLine)
                    ));
                }
                catch { }
            }
        }

        private void ParseSimple(string data)
        {
            if (string.IsNullOrEmpty(data)) return;

            // Remove spaces (example: "p1 = 10 , p2 = 20" -> "p1=10,p2=20")
            string compact = data.Replace(" ", "");

            // Split by comma
            string[] parts = compact.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries);

            bool updated = false;

            foreach (string p in parts)
            {
                if (p.StartsWith("p1=", StringComparison.OrdinalIgnoreCase))
                {
                    textBox1.Text = p.Length > 3 ? p.Substring(3) : "";
                    updated = true;
                }
                else if (p.StartsWith("p2=", StringComparison.OrdinalIgnoreCase))
                {
                    textBox2.Text = p.Length > 3 ? p.Substring(3) : "";
                    updated = true;
                }
                else if (p.StartsWith("p3=", StringComparison.OrdinalIgnoreCase))
                {
                    textBox3.Text = p.Length > 3 ? p.Substring(3) : "";
                    updated = true;
                }
                else
                {
                    // Fallback: handle formats like "p1 = 10"
                    int idx = p.IndexOf('=');
                    if (idx > 0)
                    {
                        string key = p.Substring(0, idx).ToLower();
                        string val = p.Substring(idx + 1);

                        if (key == "p1") { textBox1.Text = val; updated = true; }
                        else if (key == "p2") { textBox2.Text = val; updated = true; }
                        else if (key == "p3") { textBox3.Text = val; updated = true; }
                    }
                }
            }

            // If any value changed, record a snapshot
            if (updated)
            {
                _readings.Add(new Reading
                {
                    Time = DateTime.Now,
                    P1 = textBox1.Text,
                    P2 = textBox2.Text,
                    P3 = textBox3.Text,
                    Raw = data
                });
            }
        }

        private void button3_Click(object sender, EventArgs e) // Export CSV
        {
            try
            {
                if (_readings.Count == 0)
                {
                    MessageBox.Show("No data to export.");
                    return;
                }

                var sb = new StringBuilder();

                // CSV header
                sb.AppendLine("Time,p1,p2,p3");

                // Helper to quote fields that contain commas/quotes/newlines
                string Q(string s)
                {
                    if (s == null) return "";
                    bool needQuote = s.Contains(",") || s.Contains("\"") || s.Contains("\n") || s.Contains("\r");
                    if (!needQuote) return s;
                    return "\"" + s.Replace("\"", "\"\"") + "\"";
                }

                foreach (var r in _readings)
                {
                    sb.AppendLine($"{r.Time:yyyy-MM-dd HH:mm:ss},{Q(r.P1)},{Q(r.P2)},{Q(r.P3)}");
                }

                // Save to application (project runtime) directory
                string dir = AppDomain.CurrentDomain.BaseDirectory; // or Application.StartupPath
                string filePath = Path.Combine(dir, $"transmitted_{DateTime.Now:yyyyMMdd_HHmmss}.csv");

                File.WriteAllText(filePath, sb.ToString(), Encoding.UTF8);

                // Remember the last exported file path so we can open it later
                lastExportedFile = filePath;

                MessageBox.Show("CSV saved (openable by Excel):\n" + filePath);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Export error: " + ex.Message);
            }
        }

        private void button4_Click(object sender, EventArgs e) // Open last exported CSV
        {
            try
            {
                if (string.IsNullOrEmpty(lastExportedFile) || !File.Exists(lastExportedFile))
                {
                    MessageBox.Show("No exported file found yet, or file was moved/deleted.");
                    return;
                }

                // UseShellExecute = true guarantees opening with the default associated app (Excel)
                var psi = new ProcessStartInfo
                {
                    FileName = lastExportedFile,
                    UseShellExecute = true
                };
                Process.Start(psi);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Open file error: " + ex.Message);
            }
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            try
            {
                if (serialPort != null)
                {
                    serialPort.DataReceived -= SerialPort_DataReceived;
                    if (serialPort.IsOpen) serialPort.Close();
                    serialPort.Dispose();
                    serialPort = null;
                }
            }
            catch
            {
                // Ignore close errors
            }
        }
    }
}
