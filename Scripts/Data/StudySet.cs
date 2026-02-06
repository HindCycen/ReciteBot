using Godot;
using System;
using System.Collections.Generic;

[Serializable]
public partial class StudySet : RefCounted {
    public string Title;              // 资料名称
    public List<Chapter> Chapters;   // 章节列表

    public StudySet() {
        Chapters = new List<Chapter>();
    }
}
