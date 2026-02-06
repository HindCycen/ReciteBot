using Godot;
using System;
using System.Collections.Generic;

public partial class StudyScene : Control {
	public override void _Ready() {
		List<Chapter> _chapters = new List<Chapter> {
			new Chapter {
				Title = "导数定义",
				Content = "导数是函数在某点的变化率..."
			},
			new Chapter {
				Title = "极限思想",
				Content = "极限描述函数逼近过程..."
			}
		};

		var list = GetNode<VBoxContainer>(
			"HSplitContainer/ChapterPanel/ScrollContainer/VBoxContainer"
		);

		foreach (var chapter in _chapters) {
            var btn = new Button {
                Text = chapter.Title
            };
            btn.Pressed += () => {
				var title = GetNode<Label>(
					"HSplitContainer/ContentPanel/TitleLabel"
				);
				var content = GetNode<RichTextLabel>(
					"HSplitContainer/ContentPanel/ContentText"
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
