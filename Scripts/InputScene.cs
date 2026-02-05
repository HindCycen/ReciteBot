using Godot;
using System;
public partial class InputScene : Control {
	private TextEdit _textEdit;

	public override void _Ready() {
		_textEdit = GetNode<TextEdit>("VBoxContainer/TextEdit");

		var button = GetNode<Button>("VBoxContainer/Button");
		button.Pressed += OnGeneratePressed;
	}

	private void OnGeneratePressed() {
		string rawText = _textEdit.Text;

		GD.Print("输入文本长度: " + rawText.Length);

		// 找到 Main 场景并切换
		var main = GetTree().Root.GetNode<Main>("Main");
		main.LoadScene("res://Scenes/ProcessingScene.tscn");
	}
}