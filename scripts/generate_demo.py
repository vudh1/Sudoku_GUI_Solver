from PIL import Image, ImageDraw, ImageFont
import copy

W,H=900,520
BG=(13,17,23); PANEL=(22,27,34); TEXT=(230,237,243); MUTED=(139,148,158)
BLUE=(88,166,255); GREEN=(46,160,67); ACCENT=(255,200,80)

def font(size,bold=False,mono=False):
    base="/usr/share/fonts/truetype/dejavu/"
    if mono:
        name="DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    else:
        name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(base+name,size)

def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c]==0:
                used=set(board[r])|{board[i][c] for i in range(9)}|{board[i][j] for i in range(r//3*3,r//3*3+3) for j in range(c//3*3,c//3*3+3)}
                for n in range(1,10):
                    if n not in used:
                        board[r][c]=n
                        if solve(board): return True
                        board[r][c]=0
                return False
    return True

puzzle=[
[5,3,0,0,7,0,0,0,0],
[6,0,0,1,9,5,0,0,0],
[0,9,8,0,0,0,0,6,0],
[8,0,0,0,6,0,0,0,3],
[4,0,0,8,0,3,0,0,1],
[7,0,0,0,2,0,0,0,6],
[0,6,0,0,0,0,2,8,0],
[0,0,0,4,1,9,0,0,5],
[0,0,0,0,8,0,0,7,9],
]
solution=copy.deepcopy(puzzle); solve(solution)
empties=[(r,c) for r in range(9) for c in range(9) if puzzle[r][c]==0]
frames=[]

for i in range(62):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((34,22),"Sudoku GUI Solver",font=font(28,True),fill=TEXT)
    d.text((34,58),"Backtracking solver + unique-solution puzzle generation",font=font(16),fill=MUTED)
    d.rounded_rectangle((34,94,520,488),radius=18,fill=PANEL)
    gx,gy=64,112; gs=360; cs=gs/9
    d.rectangle((gx,gy,gx+gs,gy+gs),fill=(250,250,250))

    reveal=0 if i<7 else (len(empties) if i>54 else min(len(empties),int((i-7)/47*len(empties))))
    board=copy.deepcopy(puzzle)
    for r,c in empties[:reveal]: board[r][c]=solution[r][c]
    current=empties[reveal] if reveal<len(empties) and 7<=i<=54 else None
    if current:
        r,c=current
        d.rectangle((gx+c*cs,gy+r*cs,gx+(c+1)*cs,gy+(r+1)*cs),fill=(225,239,255))

    for g in range(10):
        width=4 if g%3==0 else 1
        col=(35,35,35) if g%3==0 else (160,160,160)
        d.line((gx+g*cs,gy,gx+g*cs,gy+gs),fill=col,width=width)
        d.line((gx,gy+g*cs,gx+gs,gy+g*cs),fill=col,width=width)

    for r in range(9):
        for c in range(9):
            v=board[r][c]
            if not v: continue
            given=puzzle[r][c]!=0
            f=font(24,given); color=(30,30,30) if given else (30,104,205)
            box=d.textbbox((0,0),str(v),font=f)
            d.text((gx+c*cs+(cs-(box[2]-box[0]))/2,gy+r*cs+(cs-(box[3]-box[1]))/2-2),str(v),font=f,fill=color)

    d.text((555,114),"SOLVER STATUS",font=font(14,True),fill=GREEN)
    status="Puzzle loaded" if reveal==0 else ("Solved" if reveal==len(empties) else "Backtracking…")
    d.text((555,148),status,font=font(27,True),fill=TEXT)
    d.text((555,193),f"Filled   {reveal:02d}/{len(empties)}",font=font(18,False,True),fill=BLUE)
    d.text((555,225),"Validation",font=font(17,True),fill=TEXT)
    d.text((555,253),"✓ row constraints",font=font(15),fill=MUTED)
    d.text((555,279),"✓ column constraints",font=font(15),fill=MUTED)
    d.text((555,305),"✓ 3×3 box constraints",font=font(15),fill=MUTED)
    d.text((555,345),"Generator",font=font(17,True),fill=TEXT)
    d.text((555,373),"Keeps a removal only",font=font(15),fill=MUTED)
    d.text((555,397),"when solution count = 1",font=font(15),fill=MUTED)
    d.rounded_rectangle((548,438,850,475),radius=12,fill=(31,38,47))
    d.text((568,447),"Unique puzzle ready" if reveal==len(empties) else "Testing candidates",font=font(15),fill=ACCENT)
    frames.append(im)

frames[0].save("demo.gif",save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True,disposal=2)
