using Godot;
using System;
using System.Diagnostics;
using System.IO;

public partial class PythonBridge : RefCounted {
    public static string RunAI(string text) {
        ProcessStartInfo psi = new ProcessStartInfo {
            FileName = "python",
            Arguments = "Scripts\\PythonScript\\api_call.py",
            RedirectStandardInput = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using Process process = new Process();
        process.StartInfo = psi;
        process.Start();

        // 发送文本给 Python
        using (StreamWriter writer = process.StandardInput) {
            writer.Write(text);
        }

        string error = process.StandardError.ReadToEnd();
        GD.PrintErr("PY ERROR: " + error);

        // 读取 AI 返回
        string output = process.StandardOutput.ReadToEnd();

        process.WaitForExit();

        return output;
    }
}
