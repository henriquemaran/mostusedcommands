# Python File Receiver e Script PowerShell para Envio de Arquivos

Este documento descreve como configurar um pequeno servidor Python para receber arquivos via HTTP POST e como enviar arquivos de uma pasta local usando PowerShell. Este sistema pode ser útil para transferências rápidas de arquivos entre máquinas na mesma rede.

---

## 📥 Parte 1: Criar o Servidor de Recebimento (Receiver)

### Objetivo

Criar um servidor Python simples que escute em uma porta específica (`8002`) e salve arquivos recebidos via HTTP POST no diretório `/opt/`.

### Código Python

Salve o código abaixo como `file_receiver.py` e execute-o com permissões de superusuário (por exemplo, `sudo python3 file_receiver.py`):

```python
# file_receiver.py
import http.server
import socketserver
import os

UPLOAD_DIR = "/opt/"
PORT = 8002

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        field_data = self.rfile.read(length)
        filename = self.headers.get('X-Filename', 'uploaded_file')

        file_path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
        with open(file_path, 'wb') as f:
            f.write(field_data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File received\n')

if __name__ == '__main__':
    os.chdir(UPLOAD_DIR)
    with socketserver.TCPServer(("", PORT), FileUploadHandler) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()
```

⚠️ **Importante**: certifique-se de que o diretório `/opt/` tem permissões de escrita para o usuário executando o script, ou execute como `sudo`.

---

## 📤 Parte 2: Enviar Arquivos via PowerShell

### Objetivo

Enviar todos os arquivos (recursivamente) de uma pasta local para o servidor Python acima, mantendo os caminhos relativos nos nomes dos arquivos enviados.

### Código PowerShell

Execute este script dentro da pasta que deseja enviar:

```powershell
Get-ChildItem -File -Recurse | ForEach-Object {
    $filePath = $_.FullName
    $relativePath = $_.FullName.Substring((Get-Location).Path.Length + 1)
    Write-Output "Enviando $relativePath..."

    $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
    $headers = @{ "X-Filename" = $relativePath }

    Invoke-WebRequest -Uri http://10.210.248.132:8002 `
                      -Method POST `
                      -Headers $headers `
                      -Body $fileBytes
}
```

🛠️ **Substitua `10.210.248.132` pelo IP da máquina que está executando o `file_receiver.py`**.

---

## ✅ Resultado Esperado

- O script Python irá salvar os arquivos recebidos dentro de `/opt/`, com o mesmo nome e estrutura relativa usados no envio.
- O script PowerShell imprimirá no terminal o nome de cada arquivo enviado com sucesso.

---

## 🔐 Segurança

Este método **não possui autenticação** nem criptografia. Use apenas em redes locais seguras ou para testes internos. Para produção, considere usar HTTPS e autenticação.

