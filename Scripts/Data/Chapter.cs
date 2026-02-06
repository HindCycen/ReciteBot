using Godot;
using System;

[Serializable]
public partial class Chapter : RefCounted {
    public string Title { get; set; }
    public string Content { get; set; }

    public Chapter() { }

    public Chapter(string title, string content) {
        Title = title;
        Content = content;
    }
}
