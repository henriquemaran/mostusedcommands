# 📦 Registro de Serviço systemd no RHEL 7.9 para um script Python

## ✅ 1. Pré-requisitos

### Verifique se o Python 3 está instalado:
```bash
which python3
```

### Torne o script executável:
```bash
sudo chmod +x /opt/oi/receiver.py
```

---

## ✅ 2. Crie o arquivo do serviço

```bash
sudo nano /etc/systemd/system/receiver.service
```

Cole o seguinte conteúdo:

```ini
[Unit]
Description=Receiver Python Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/oi/receiver.py
WorkingDirectory=/opt/oi
Restart=on-failure
RestartSec=5
User=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

> 💡 Se quiser rodar como outro usuário, troque `User=root` pelo nome do usuário.

---

## ✅ 3. Recarregue o systemd

```bash
sudo systemctl daemon-reload
```

---

## ✅ 4. Ative o serviço

```bash
sudo systemctl enable receiver.service
```

---

## ✅ 5. Inicie o serviço

```bash
sudo systemctl start receiver.service
```

---

## ✅ 6. Verifique o status

```bash
sudo systemctl status receiver.service
```

---

## ✅ 7. Veja os logs (opcional)

```bash
journalctl -u receiver.service -n 50 --no-pager
```

---

## 🛠️ Se alterar o script ou o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl restart receiver.service
```

---

## ✅ Pronto!
Seu serviço Python agora está registrado corretamente no systemd e será iniciado automaticamente com o sistema.
