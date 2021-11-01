class StrumPattern:
    def __init__(self, pattern, bars_covered=1,time=4, posative="/", negative = ".", mute = "!"):
        self.bars_covered = bars_covered
        self.time = time
        self.pattern=pattern
        self.out=[]
        for i in time:
            if self.pattern[i]=="posative":
                self.repr.append(True)
            elif self.pattern[i]=="negative":
                self.out.append(False)
            
    def __str__(self):
        return self.pattern
    def __repr__(self):
        pass
    def __getitem__(self, key: int) -> ReturnType:
        pass
    