using Godot;
using System;
using System.Collections.Generic;

public partial class StudyScene : Control {
	public override void _Ready() {
        var set = new StudySet {
            Title = "Test Notes"
        };

        set.Chapters.Add(new Chapter(
			"Chapter 1",
			"Summary of chapter 1"
		));

		set.Chapters.Add(new Chapter(
			"Chapter 2",
			"Summary of chapter 2"
		));

		StudyManager.Instance.LoadStudySet(set);

		List<Chapter> _chapters = StudyManager.Instance.GetChapters();

		var list = GetNode<VBoxContainer>(
			"HSplitContainer/ChapterPanel/ScrollContainer/VBoxContainer"
		);

		foreach (var chapter in _chapters) {
			var btn = new Button {
				Text = chapter.Title
			};
			btn.Pressed += () => {
				var title = GetNode<Label>(
					"HSplitContainer/ContentPanel/VBoxContainer/TitleLabel"
				);
				var content = GetNode<RichTextLabel>(
					"HSplitContainer/ContentPanel/VBoxContainer/ScrollContainer/ContentText"
				);

				title.Text = chapter.Title;
				content.Text = chapter.Content;
			};
			list.AddChild(btn);
		}
	}

	public override void _Process(double delta) {
	}
}
