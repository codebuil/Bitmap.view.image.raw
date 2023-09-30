import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import math

# Função para abrir uma imagem raw
def abrir_imagem_raw():
    global imagem_original
    global imagem_convertida

    file_path = filedialog.askopenfilename(filetypes=[("Imagens RAW", "*.raw")])
    if file_path:
        tamanho_arquivo = os.path.getsize(file_path)
        tamanho_lado = int(math.sqrt(tamanho_arquivo))

        if tamanho_lado * tamanho_lado != tamanho_arquivo:
            erro_label.config(text="Erro: O arquivo não é quadrado")
        else:
            imagem_original = Image.new("P", (tamanho_lado, tamanho_lado))

            with open(file_path, "rb") as file:
                for y in range(tamanho_lado):
                    for x in range(tamanho_lado):
                        byte = file.read(1)
                        cor = int.from_bytes(byte, byteorder="big")
                        imagem_original.putpixel((x, y), cor)

            imagem_convertida = converter_imagem(imagem_original)
            imagem_convertida = ImageTk.PhotoImage(imagem_convertida)
            imagem_label.config(image=imagem_convertida)
            imagem_label.imagem = imagem_convertida
            erro_label.config(text="")

# Função para converter a imagem
def converter_imagem(imagem):
    largura, altura = imagem.size
    imagem_convertida = Image.new("RGB", (largura, altura))

    for x in range(largura):
        for y in range(altura):
            cor = imagem.getpixel((x, y))
            cor_rgb = cores_vga[cor]
            imagem_convertida.putpixel((x, y), cor_rgb)

    return imagem_convertida

# Tabela de cores VGA
cores_vga = [
    (0, 0, 0),        # Preto
    (0, 0, 168),      # Azul
    (0, 168, 0),      # Verde
    (0, 168, 168),    # Ciano
    (168, 0, 0),      # Vermelho
    (168, 0, 168),    # Magenta
    (168, 84, 0),     # Marrom
    (168, 168, 168),  # Cinza claro
    (84, 84, 84),     # Cinza escuro
    (84, 84, 255),    # Azul claro
    (84, 255, 84),    # Verde claro
    (84, 255, 255),   # Ciano claro
    (255, 84, 84),    # Vermelho claro
    (255, 84, 255),   # Magenta claro
    (255, 255, 84),   # Amarelo
    (255, 255, 255)   # Branco
]

# Criar a janela principal
janela = tk.Tk()
janela.title("Visualizador de Imagens RAW")
janela.geometry("400x400")
janela.configure(bg="blue")

# Botão para abrir uma imagem RAW
botao_abrir = tk.Button(janela, text="Abrir Imagem RAW", command=abrir_imagem_raw)
botao_abrir.pack(pady=20)

# Rótulo para exibir a imagem
imagem_label = tk.Label(janela)
imagem_label.pack()

# Rótulo para exibir mensagens de erro
erro_label = tk.Label(janela, fg="red")
erro_label.pack()

imagem_original = None
imagem_convertida = None

janela.mainloop()
