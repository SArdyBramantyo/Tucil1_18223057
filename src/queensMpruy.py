import time
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from PIL import ImageGrab

class exhaustive_search:
    def __init__(self, file_input, gui):
        f = open(file_input, 'r')
        konten_file = f.readlines()
        f.close()

        self.board = []
        for line in konten_file:
            line = line.strip()
            if line != "":
                self.board.append(list(line))
        
        self.n = len(self.board)
        
        warna_unik = set()
        for i in range(self.n):
            for j in range(self.n):
                warna_unik.add(self.board[i][j]) # Karena bersifat set, maka tidak akan menambahkan warna yang sama
        
        if len(warna_unik) != self.n:
            raise ValueError("Input Invalid!")
        
        else:
            self.board_copy = self.board
        
        self.gui = gui
    
    def algoritma_ES(self):
        posisi_Q_papan = []
        for i in range(self.n):
            for j in range(self.n):
                posisi_Q_papan.append((i,j))
        
        num_of_posisi = len(posisi_Q_papan)
        queen = list(range(self.n))

        array_of_combination = []
        while True:
            temp = []
            for i in range(self.n):
                temp.append(posisi_Q_papan[queen[i]])
            array_of_combination.append(temp) # Untuk mencatat kombinasi dari setiap queen

            idx = self.n - 1
            while idx >= 0:
                if queen[idx] != idx + (num_of_posisi - self.n):
                    break
                else:
                    idx -= 1

            if idx < 0: # udah mentok
                break 

            else:
                queen[idx] += 1 # maju
                if idx != (self.n - 1): 
                    for i in range(idx+1, self.n): # reset kalau bukan ujung aja
                        queen[i] = queen[i-1] + 1
        
        time_start = time.time()
        iterasi = 0
        interval = max(1000, len(array_of_combination) // 120) # 10% kurleb ceunah

        for combination in array_of_combination:
            iterasi += 1
            if iterasi % interval == 0:
                print(f"\nIterasi ke-{iterasi}")
                result = []
                for i in range(self.n):
                    row = []
                    for j in range(self.n):
                        row.append(self.board[i][j])
                    result.append(row)
                for i, j in combination:
                    result[i][j] = '#' # Queen

                for i in result:
                    print(' '.join(i))
                
                time_end = (time.time()-time_start) * 1000
                if self.gui:
                    self.gui(self.board_copy, result, time_end, iterasi, True)
                time.sleep(0.15)
            
            if self.validate(combination) == True:
                print(f"\nIterasi ke-{iterasi}")
                result = []
                for i in range(self.n):
                    row = []
                    for j in range(self.n):
                        row.append(self.board[i][j])
                    result.append(row)
                for i, j in combination:
                    result[i][j] = '#'

                for i in result:
                    print(' '. join(i))
                time_end = (time.time()-time_start) * 1000
                print(f"\nWaktu pencarian: {time_end:.2f} ms")
                print(f"Banyak kasus yang ditinjau: {iterasi} kasus")
                f= open('solution.txt', 'w')
                for i in result:
                    f.write(''.join(i)+'\n')
                f.close()

                if self.gui:
                    self.gui(self.board_copy, result, time_end, iterasi, True)
                return True
            
        time_end = (time.time()-time_start) * 1000
        print(f"\n Tidak ada solusi")
        print(f"Waktu pencarian: {time_end:.2f} ms")
        print(f"Banyak kasus yang ditinjau: {iterasi} kasus")
        if self.gui:
            self.gui(self.board_copy, None, time_end, iterasi, False)
        return False

    
    def validate(self, queen_combination):
        # 1. Horizontal
        horizontal=[]
        horizontal_unik=set()
        for i in queen_combination:
            horizontal.append(i)
            horizontal_unik.add(i)
        if len(horizontal) != len(horizontal_unik):
            return False
        
        #2. Vertikal
        vertikal=[]
        vertikal_unik=set()
        for i in queen_combination:
            vertikal.append(i)
            vertikal_unik.add(i)
        if len(vertikal) != len(vertikal_unik):
            return False

        #3. Diagonal
        for ref in range(len(queen_combination)):
            for ref_kanan in range(ref+1, len(queen_combination)):
                x_r, y_r = queen_combination[ref]
                x_rk, y_rk = queen_combination[ref_kanan]
                if (abs(x_r-x_rk) <=1) and (abs(y_r-y_rk) <=1):
                    return False
        
        #4. Warna
        warna=[]
        warna_unik=set()
        for i in queen_combination:
            warna.append(self.board[i[0]][i[1]])
            warna_unik.add(self.board[i[0]][i[1]])
        if len(warna) != len(warna_unik):
            return False
        
        return True

class gui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        header = tk.Frame(root) # header, untuk functional button
        header.pack(fill=tk.X)
        up_file = tk.Button(header, text="Upload File", command=self.upload, bg='light blue', fg='black', padx=20)
        up_file.pack(side=tk.LEFT)
        solve_btn =tk.Button(header, text="Solusi!", command=self.solve, bg='green', fg='white', padx=20)
        solve_btn.pack(side=tk.LEFT, padx=5)

        body=tk.Frame(root, bg='black') # body, buiat tampilin gambar
        body.pack(fill=tk.BOTH, expand=True)
        kontainer_input = tk.Frame(body, bg='black')
        kontainer_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.input_board = tk.Canvas(kontainer_input, bg='beige', width=400, height=400)
        self.input_board.pack(pady=5)
        kontainer_output = tk.Frame(body, bg='black')
        kontainer_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.output_board = tk.Canvas(kontainer_output, bg='beige', width=400, height=400)
        self.output_board.pack(pady=5)
        
        footer= tk.Frame(root, bg='light blue', pady=15) # footer, buat stats aja
        footer.pack(fill=tk.X)
        self.stats = tk.Label(footer, text="stats: ", bg='light blue', fg='black')
        self.stats.pack()

        self.file_path = None
        self.algorithm = None

        self.pallete = { # me ji ku hi bi ni u
            'A': "#750707",
            'B': "#976810",
            'C': "#85852c",
            'D': '#008000', 
            'E': "#28a228",
            'F': '#000080',
            'G': "#187b71",
            'H': "#5f047d",
            'I': "#a84576",
        }

    def upload(self):
        file_input = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], )
        self.input_board.delete("all")
        self.output_board.delete("all")

        if file_input:
            try:
                self.file_path=file_input
                self.algorithm=exhaustive_search(file_input, self.update)
                self.gambar(self.algorithm.board_copy, self.algorithm.board, self.input_board)
            
            except ValueError:
                messagebox.showerror("File Invalid")
                self.file_path=None
                self.algorithm=None
    
    def solve(self):
        if self.algorithm:
            self.root.update()
            t = threading.Thread(target=exhaustive_search(self.file_path, self.update).algoritma_ES)
            t.daemon =True
            t.start()

        else:
            messagebox.showwarning("File Invalid!")
            return
    
    def update(self, board_awal, board_akhir, time, iterasi, found):
        if found:
            self.gambar(board_awal, board_akhir, self.output_board)
            self.stats.config(text=f"Waktu pencarian: {time:.2f} ms & Banyak tinjuan: {iterasi} kasus")
            self.root.after(40, lambda: self.screenshot(self.output_board))

            
        else:
            self.output_board.delete("all")
            self.output_board.create_text(200, 200, text="Tidaak ada solusi!", fill='red')
            self.stats.config(text=f"Waktu pencarian: {time:.2f} ms & Banyak tinjuan: {iterasi} kasus")

    def gambar(self, board_awal, board_akhir, kontainer):
        kontainer.delete("all")
        if board_akhir:

            n=len(board_akhir)
            ukuran=min(500//n, 50)
            for i in range(n):
                for j in range(n):
                    x_1=(j*ukuran) + 5
                    y_1=(i*ukuran) + 5
                    x_2=(x_1+ukuran)
                    y_2=(y_1+ukuran)

                    warna_akhir= board_akhir[i][j]
                    if warna_akhir=='#': # Queen
                        warna_awal= board_awal[i][j]
                        kontainer.create_rectangle(x_1,y_1,x_2,y_2, fill=self.pallete.get(warna_awal, 'white'))
                        kontainer.create_text((x_1+x_2)/2, (y_1+y_2)/2, text='Q', fill='white', font=('Arial', 18, 'bold'))
                    
                    else: #Warna biasa
                        kontainer.create_rectangle(x_1,y_1,x_2,y_2, fill=self.pallete.get(warna_akhir, 'white'))
    
    def screenshot(self, kontainer):
        x=kontainer.winfo_rootx()
        y=kontainer.winfo_rooty()
        x_1=x+ kontainer.winfo_width()
        y_1=y+ kontainer.winfo_height()
        ImageGrab.grab(bbox=(x,y,x_1,y_1)).save("solution.png")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file=sys.argv[1]
        solusi = exhaustive_search(file_input=file).algoritma_ES()
    else:
        root= tk.Tk()
        app= gui(root)
        root.mainloop()

