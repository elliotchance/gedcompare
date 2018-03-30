# gedcompare

`gedcompare` will compare two GEDCOM files and print out the differences:

![Screenshot](https://raw.githubusercontent.com/elliotchance/gedcompare/master/screenshot.png)

Usage
-----

```bash
gedcompare.py file1.ged file2.ged
```

Legend
------

**Attributes**

Icon | Description
---- | -----------
🚻   | Gender
♂️    | Male
♀️    | Female
📛   | Name

**Life events**

Icon | Description
---- | -----------
👶   | Birth
⛪   | Christening
🏠   | Residence (not yet implemented)
🔨   | Occupation (not yet implemented)
💑   | Marriage (not yet implemented)
⚮   | Divorce (not yet implemented)
✝️    | Death
⚰️    | Burial

**Comparison**

Icon | Description
---- | -----------
↔️    | Value differs on both sides
⬅️   | Only left has value
➡️    | Only right has value
