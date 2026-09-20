import numpy as np

#s-box table Substitution table
s_box = np.array([
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]
], dtype=np.uint8)

#r-con table Round constant table
rcon = np.array([
    [0x01, 0x00, 0x00, 0x00],
    [0x02, 0x00, 0x00, 0x00],
    [0x04, 0x00, 0x00, 0x00],
    [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00],
    [0x20, 0x00, 0x00, 0x00],
    [0x40, 0x00, 0x00, 0x00],
    [0x80, 0x00, 0x00, 0x00],
    [0x1B, 0x00, 0x00, 0x00],
    [0x36, 0x00, 0x00, 0x00]
], dtype=np.uint8)

#funções para manipular os valores hexadecimais
def char_hex(c):
    return ord(c)

def hex_to_char(h):
    return chr(h)

def hex_low(h): #pega os 4 bits menos significativos
    return h & 0x0F

def hex_high(h): #pega os 4 bits mais significativos do número hexadecimal
    return h >> 4

def hex_idx(h, axis):
    if axis: #axis == 1, o eixo do hex_low (parte direita do hexadecimal)
        return hex_low(h)
    return hex_high(h) #axis == 0, mesmo do hex_high

#Função para rotacionar uma palavra (vetor de 4 bytes) para a esquerda
def rot_word(w: np.array):
    return np.roll(w, -1)

#Função para aplicar a substituição de bytes em uma palavra (vetor de 4 bytes) usando a s-box
def sub_word(w: np.array):
    w_sub = w.copy()
    for i in range(w.shape[0]):
        hex_a = w_sub[i]
        ax0 = hex_high(hex_a)
        ax1 = hex_low(hex_a)
        w_sub[i] = s_box[ax0, ax1]
    return w_sub


# função para multiplicação em GF(2^7)
# https://en.wikipedia.org/wiki/Finite_field_arithmetic
def gf_mul(a: np.uint8, b: np.uint8) -> np.uint8:
    p = 0 # produto acumulado
    while a != 0 and b != 0:
        # adição polinomial
        if b & 1:
            p ^= a
        b >>= 1 # divide o polinômio por x

        carry = a & 0x80 # armazena se o bit mais significativo de a é igual a um 1
        a <<= 1 # multiplica o polinômio por x
        if(carry):
            a ^= 0x1b # 0x1b corresponde ao polinômio irredutível sem o termo maior

    return p

#Função para expandir a chave de 16 bytes (128 bits) em 44 palavras (4 bytes cada) para o AES-128
def key_expansion(key: np.array):

    w = np.zeros((4, 44), dtype=np.uint8)
    w[:, :4] = key.reshape(4, 4).T

    for i in range(4, 44):
        temp = w[:, i - 1].copy()

        if i % 4 == 0:
            temp = sub_word(rot_word(temp)) ^ rcon[i // 4 - 1]

        w[:, i] = w[:, i - 4] ^ temp

    return w
        

def key_add(A, k): #
    #A é a matrix estado com elementos em hexadecimal
    #k é a subchave do tamanho de A com elementos em hexadecimal
    #Cada elemento do GF(2^7) é um Byte representado em vetor de 8bits (representação matemática de um polinomio), e é feito a soma modulo 2 entre eles na operação de soma (equivale a xor)
    return np.bitwise_xor(A,k)
    
#Função que substitui os bytes usando uma tabela com resultados de s-box
def byte_sub(A:np.array): #A é a matrix de estado de hexadecimais
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            hex_a = A[i,j]
            #ex: se a = "P" = 0x50
            ax0 = hex_idx(hex_a, 0) #ax0 = 5
            ax1 = hex_idx(hex_a, 1) #ax1 = 0
            A[i,j] = s_box[ax0,ax1] #s_box(5,0) = 0x53 = "S"
            #então a = "P" -> s_box -> "S", no entanto nem todas as transformações resultam em caracteres imprimíveis.
    return A #matrix de estado modificada

#tabela para s-box e galois field, o inverso você olha para o valor resultante e depois para o que resultou
def inv_byte_sub(A:np.array): #inverte a transformação da substituição de byte
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            hex_a = A[i,j]
            #ex: se a = "S" = 0x53
            linha, col = np.where(s_box == hex_a) #descobre valores que geraram hex_a procurando ele na tabela
            A[i,j] = (linha << 4) +col # linha = 5, col = 3, A[i,j] = 0x53
            #então a = "S" -> "inv_s_box" -> "P", no entanto nem todas as transformações resultam em caracteres imprimíveis.
    return A #matrix de estado modificada
def rows_shift(A:np.array):
    A[1,0], A[1,1], A[1,2], A[1,3] = A[1,1], A[1,2], A[1,3], A[1,0]
    A[2,0], A[2,1], A[2,2], A[2,3] = A[2,2], A[2,3], A[2,0], A[2,1]
    A[3,0], A[3,1], A[3,2], A[3,3] = A[3,3], A[3,0], A[3,1], A[3,2]
def columns_mix(A:np.array):
    result = np.zeros((4,), dtype=np.uint8)
    mat = np.array([2, 3, 1, 1], dtype=np.uint8)

    for i in range(4):
        col = A[:,i]
        result[0] = gf_mul(mat[0],col[0])^gf_mul(mat[1],col[1])^gf_mul(mat[2],col[2])^gf_mul(mat[3],col[3])
        result[1] = gf_mul(mat[3],col[0])^gf_mul(mat[0],col[1])^gf_mul(mat[1],col[2])^gf_mul(mat[2],col[3])
        result[2] = gf_mul(mat[2],col[0])^gf_mul(mat[3],col[1])^gf_mul(mat[0],col[2])^gf_mul(mat[1],col[3])
        result[3] = gf_mul(mat[1],col[0])^gf_mul(mat[2],col[1])^gf_mul(mat[3],col[2])^gf_mul(mat[0],col[3])
        A[:,i] = result

def test():
    # ==========================================
    # TESTE DA EXPANSÃO DE CHAVE
    # ==========================================
    if __name__ == "__main__":
        # 1. A chave de teste fornecida
        key_hex_string = "6D727561766564703132333435363738"
        
        # 2. Converte a string hexadecimal em um array de 16 bytes (uint8)
        key_bytes = np.array([int(key_hex_string[i:i+2], 16) for i in range(0, 32, 2)], dtype=np.uint8)
        
        # 3. Chama a sua função!
        chaves_expandidas = key_expansion(key_bytes)
        
        # 4. Extrai a chave da Rodada 1 (colunas 4 a 7 da matriz w)
        round_1_key_matrix = chaves_expandidas[:, 4:8]
        
        # 5. Formata a saída de volta para string Hexadecimal para conferir
        # Transpõe (.T) e achata (.flatten()) para ler na ordem correta
        round_1_hex = "".join(f"{byte:02X}" for byte in round_1_key_matrix.T.flatten())
        
        print("--- RESULTADO DO TESTE ---")
        print(f"Chave Inicial: {key_hex_string.upper()}")
        print(f"Chave Rodada 1 Calculada: {round_1_hex}")
        
        # O resultado esperado matemático para essa chave no AES
        expected = "69E872F71F8D16872EBF25B31B89128B"
        if round_1_hex == expected:
            print("✅ SUCESSO! A sua Expansão de Chave está perfeita!")
        else:
            print(f"❌ ERRO! O esperado era: {expected}")

def make_matrix(A, it_is_hex): #A é uma string, com letras ou valores que representam hexadecimais
    matrix = np.zeros((4,4), dtype=np.uint8)
    if it_is_hex:
        for i in range(4):
            for j in range(4):
                matrix[j,i] = int(A[(i*4+j)*2:(i*4+j+1)*2],16) #pega de 2 em 2 bytes
    else:
        for i in range(4):
            for j in range(4):
                matrix[j,i] = ord(A[i*4+j])
    return matrix

def fbf_to_hex_string(matrix): #transforma matrix 4x4 em uma string em que cada par de letras representa um hexadecimal (o inverso do make_matrix)
    A = np.zeros((4,4), dtype=np.uint8) 
    for i in range(4):
        for j in range(4):
            A[i,j] = matrix[j,i]
    hex_string = ''.join(f'{x:02x}' for x in A.flatten())
    return hex_string

def cifrar(msg, k, key_is_hex):
    A = make_matrix(msg, False)
    
    if key_is_hex: #transforma a chave em uma array de valores
        key = np.array([int(k[i:i+2], 16) for i in range(0, 32, 2)], dtype=np.uint8)
    else:
        key = np.array([ord(k[i]) for i in range(len(k))], dtype=np.uint8)
    w = key_expansion(key) #gera subchaves e colocar em uma matrix w

    k_mat = np.zeros((4,4), dtype=np.uint8) #coloca a chave em uma matrix para conseguir fazer a adição de chave
    for i in range(4):
        for j in range(4):
            k_mat[j,i] = key[i*4+j]
    A = key_add(A,k_mat) #adiciona k0, round 0
    for i in range(1,11): #10 rounds porque a chave tem 128 bits
        A = byte_sub(A)
        rows_shift(A)
        if i != 10: #omite na última rodada
            columns_mix(A)
        sub_key = w[:, i*4:(i+1)*4]
        A = key_add(A,sub_key)
    hex_string = fbf_to_hex_string(A)
    return hex_string #string hexadecimal