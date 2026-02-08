using Godot;
using System;
public partial class InputScene : Control {
	private TextEdit _textEdit;

	public override void _Ready() {
		_textEdit = GetNode<TextEdit>("VBoxContainer/TextEdit");

		var button = GetNode<Button>("VBoxContainer/Button");
		button.Pressed += () => {
			string rawText = _textEdit.Text;

			var main = GetTree().Root.GetNode<Main>("Main");
			main.LoadScene("res://Scenes/ProcessingScene.tscn");
			
			System.Threading.Tasks.Task.Run( () => {
				string output = PythonBridge.RunAI(rawText);
				CallDeferred(nameof(OnAIResult), output);
			});
		};
	}

	private static void OnAIResult(string output) {
		GD.Print("AI 输出: " + output);
	}

}