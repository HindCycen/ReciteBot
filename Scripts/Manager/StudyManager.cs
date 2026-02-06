using Godot;
using System.Collections.Generic;
using System;
using System.Text.Json;

[GlobalClass]
public partial class StudyManager : Node {
    public static StudyManager Instance;

    public StudySet CurrentSet = new();

    public override void _Ready() {
        Instance = this;
    }

    public void LoadStudySet(StudySet set) {
        CurrentSet = set;
    }

    public List<Chapter> GetChapters() {
        return CurrentSet.Chapters;
    }

    public void SaveToFile(string path) {
        string json = JsonSerializer.Serialize(
            CurrentSet,
            new JsonSerializerOptions { WriteIndented = true }
        );

        FileAccess file = FileAccess.Open(path, FileAccess.ModeFlags.Write);
        file.StoreString(json);
    }
    
    public void LoadFromFile(string path) {
        if (!FileAccess.FileExists(path)) { return; }

        FileAccess file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
        string json = file.GetAsText();

        CurrentSet = JsonSerializer.Deserialize<StudySet>(json);
    }

}
