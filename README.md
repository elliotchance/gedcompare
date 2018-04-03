# gedcompare

`gedcompare` will compare two GEDCOM files and print out the differences:

![Screenshot](https://raw.githubusercontent.com/elliotchance/gedcompare/master/screenshot.png)

Usage
-----

```bash
gedcompare.py file1.ged file2.ged
```

You may also use the following options:

```txt
-h, --help            show this help message and exit
--compare COMPARE     comma-separated list of attributes to compare,
                      defaults to all of:
                        birth  = birth date and place
                        burial = burial date and place
                        death  = death date and place
                        gender = gender/sex
                        name   = first and last name
--direction DIRECTION
                      show differences from the "left", "right" or "both"
                      (default is "both")
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
