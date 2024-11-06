# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Victor Cassiano de Freitas
#    Matrícula: 202203533
#    Turma: CC5N
#    Email: victorcassiano191@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        """
        Inicializa uma nova instância de imagem com largura e altura especificadas
        e uma lista de pixels fornecida.
        
        Parâmetros:
            largura (int): A largura da imagem em pixels.
            altura (int): A altura da imagem em pixels.
            pixels (list): Lista contendo os valores dos pixels da imagem.
        """
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        """
        Retorna o valor do pixel na posição (x, y) na imagem.
        
        Parâmetros:
            x (int): A posição x do pixel.
            y (int): A posição y do pixel.
        
        Retorno:
            int: Valor do pixel na posição especificada.
        """
        index = y * self.largura + x
        return self.pixels[index]
    
    def get_pixel2(self, x, y):
        """
        Retorna o valor do pixel na posição (x, y) após limitar x e y
        aos limites da imagem para evitar erros de indexação.
        
        Parâmetros:
            x (int): A posição x do pixel.
            y (int): A posição y do pixel.
        
        Retorno:
            int: Valor do pixel dentro dos limites da imagem.
        """
        x_limitado = max(0, min(x, self.largura - 1))
        y_limitado = max(0, min(y, self.altura - 1))
        
        index = y_limitado * self.largura + x_limitado
        return self.pixels[index]


    def set_pixel(self, x, y, c):
        """
        Define o valor do pixel na posição (x, y) para o valor especificado.
        
        Parâmetros:
            x (int): A posição x do pixel.
            y (int): A posição y do pixel.
            c (int): O novo valor a ser definido para o pixel.
        """
        index = y * self.largura + x
        self.pixels[index] = c


    def aplicar_por_pixel(self, func):
        """
        Cria uma nova imagem aplicando uma função a cada pixel da imagem atual.
        
        Parâmetros:
            func (callable): Função que recebe o valor de um pixel e retorna
            o novo valor transformado.
        
        Retorno:
            Imagem: Nova instância de imagem com pixels modificados pela função.
        """
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            nova_cor = ""
            for y in range(resultado.altura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado
    
    def invertida(self):
        """
        Gera uma nova imagem invertendo o valor de cada pixel.
        Cada valor de pixel é transformado pela operação 255 - c,
        onde c é o valor original do pixel.
        
        Retorno:
            Imagem: Nova instância de imagem com os valores dos pixels invertidos.
        """
        return self.aplicar_por_pixel(lambda c: 255 - c)

    def correlacoes(self, kernel, arredondar=True):
        """
        Aplica uma operação de correlação na imagem com o kernel fornecido,
        gerando uma nova imagem como resultado. O kernel é uma matriz
        de pesos que é aplicada a cada pixel da imagem.
        
        Parâmetros:
            kernel (list of list): Matriz usada para realizar a correlação.
            arredondar (bool): Indica se os valores de saída devem ser arredondados
            e limitados entre 0 e 255 (padrão é True).
        
        Retorno:
            Imagem: Nova instância de imagem após a aplicação da correlação.
        """
        tamanho_kernel = len(kernel)
        deslocamento = tamanho_kernel // 2  
        nova_imagem = Imagem.nova(self.largura, self.altura)

        for y in range(self.altura):
            for x in range(self.largura):
                soma = 0
                for linha in range(tamanho_kernel):
                    for coluna in range(tamanho_kernel):
                        pixel_x = x + coluna - deslocamento
                        pixel_y = y + linha - deslocamento
                        valor_pixel = self.get_pixel2(pixel_x, pixel_y)
                        valor_kernel = kernel[linha][coluna]
                        soma += valor_pixel * valor_kernel
                if arredondar:
                    nova_imagem.set_pixel(x, y, min(max(round(soma), 0), 255))
                else: 
                    nova_imagem.set_pixel(x, y, soma)
        
        return nova_imagem
    
    def gerar_kernel_nxn(self, n):
        """
        Gera um kernel de média de tamanho nxn.
        
        Parâmetros:
            n (int): Tamanho do kernel (nxn).
        
        Retorno:
            list: Kernel de média de tamanho nxn.
        """
        return [[1 / (n * n) for _ in range(n)] for _ in range(n)]
        
    def borrada(self, n):
        """
        Aplica um efeito de borrão na imagem usando um kernel de média de tamanho nxn.
        
        Parâmetros:
            n (int): Tamanho do kernel de borrão (nxn).
        
        Retorno:
            Imagem: Nova instância de imagem com o efeito de borrão aplicado.
        """
        kernel = self.gerar_kernel_nxn(n)
        
        return self.correlacoes(kernel)

    def focada(self, n):
        """
        Aplica um efeito de foco na imagem usando um kernel de borrão e uma fórmula
        que realça a diferença entre a imagem original e a imagem borrada.
        
        Parâmetros:
            n (int): Tamanho do kernel de borrão (nxn) utilizado para o cálculo do foco.
        
        Retorno:
            Imagem: Nova instância de imagem com o efeito de foco aplicado.
        """
        kernel = self.gerar_kernel_nxn(n)
        
        imagem_borrada = self.correlacoes(kernel)
        
        nova_imagem = Imagem.nova(self.largura, self.altura)
        
        for x in range(self.largura):
            for y in range(self.altura):
                valor_original = self.get_pixel(x, y)
                valor_borrado = imagem_borrada.get_pixel(x, y)
                
                valor_focado = round(2 * valor_original - valor_borrado)
                
                nova_imagem.set_pixel(x, y, min(max(valor_focado, 0), 255))
        
        return nova_imagem


    def bordas(self):
        """
        Realça as bordas na imagem aplicando a detecção de bordas de Sobel.
        Usa dois kernels (Kx e Ky) para calcular a magnitude do gradiente,
        identificando bordas horizontais e verticais.
        
        Retorno:
            Imagem: Nova instância de imagem com as bordas destacadas.
        """
        kx = [
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ]
        
        ky = [
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ]

        imagem_kx = self.correlacoes(kx, False)
        imagem_ky = self.correlacoes(ky, False)

        nova_imagem = Imagem.nova(self.largura, self.altura)

        for x in range(self.largura):
            for y in range(self.altura):
                valor_kx = imagem_kx.get_pixel(x, y)
                valor_ky = imagem_ky.get_pixel(x, y)

                valor_borda = min(max(round(math.sqrt(valor_kx**2 + valor_ky**2)), 0), 255)
                
                nova_imagem.set_pixel(x, y, valor_borda)

        return nova_imagem
        

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    """
    TESTE 1
    imagem = Imagem.carregar("test_images/centered_pixel.png")
    imagem_invertida = imagem.invertida()
    imagem_invertida.mostrar()

    TESTE 2 (QUESTÃO 2) 
    imagem = Imagem.carregar("test_images/bluegill.png")
    imagem.mostrar()

    imagem_borda = imagem.invertida()
    imagem_borda.salvar("./imagens_questoes/bluegill_invertida.png")

    TESTE 3 (QUESTÃO 4)
    imagem = Imagem.carregar("test_images/pigbird.png")
    imagem.mostrar()

    kernel = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    imagem_correlacoes = imagem.correlacoes(kernel)
    imagem_correlacoes.salvar("./imagens_questoes/pigbird_correlacionado.png")

    TESTE 4
    imagem = Imagem.carregar("test_images/cat.png")
    imagem.mostrar()

    imagem_borrada = imagem.borrada(5)
    imagem_borrada.salvar("./imagens_questoes/cat_borrado2.png")
    
    
    #TESTE 5
    imagem = Imagem.carregar("test_images/python.png")
    imagem.mostrar()

    imagem_focada = imagem.focada(11)
    imagem_focada.salvar("./imagens_questoes/python_focado.png")
    

    #TESTE 5
    imagem = Imagem.carregar("test_images/chess.png")

    resultado = Imagem.carregar("test_results/chess_edges.png")
    resultado.mostrar()

    imagem_borda = imagem.bordas()
    imagem_borda.mostrar()
    
    #TESTE6:
    imagem = Imagem.carregar("test_images/construct.png")
    imagem.mostrar()

    imagem_borda = imagem.bordas()
    imagem_borda.salvar("./imagens_questoes/construct_bordas.png")

    #TESTE COM UMA FOTO MINHA
    imagem = Imagem.carregar("test_images/usss.png")

    invertida = imagem.invertida()
    invertida.mostrar()

    borrada = imagem.borrada(5)
    borrada.mostrar()

    focada = imagem.focada(11)
    focada.mostrar()

    borda = imagem.bordas()
    borda.mostrar()
    """
    
    
    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
