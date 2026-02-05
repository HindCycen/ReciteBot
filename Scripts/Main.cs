using Godot;
using System;

public partial class Main : Control {
	private Control _sceneRoot;

	public override void _Ready() {
		_sceneRoot = GetNode<Control>("SceneRoot");
		LoadScene("res://Scenes/InputScene.tscn");
	}

	public void LoadScene(string path) {
		foreach (Node child in _sceneRoot.GetChildren()) {
			child.QueueFree();
		}
		var scene = GD.Load<PackedScene>(path);
		var instance = scene.Instantiate();
		_sceneRoot.AddChild(instance);
	}
}
