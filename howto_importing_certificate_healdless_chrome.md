Step-by-step: Import .pfx directly for Chromium headless

1. 🔧 Create a new Chromium user data dir (NSS DB will live here)

    ```bash
    mkdir -p ~/chromium-client-profile
    ```

2. 🔑 Import the .pfx using pk12util  
   Make sure you have nss-tools installed:

    ```bash
    sudo dnf install nss-tools
    ```

   Then:

    ```bash
    pk12util -d sql:~/chromium-client-profile \
             -i T903000.pfx \
             -W your_pfx_password
    ```
   Replace `your_pfx_password` with the password for the `.pfx` file.

3. ✅ Confirm the cert is available

    ```bash
    certutil -L -d sql:~/chromium-client-profile
    ```
   Look for the alias (often it's the CN of the cert, e.g. `"Test-User AT-t903000"`).

4. 🚀 Launch Chromium in `--headless=new` mode using this profile

    ```bash
    chromium-browser \
      --user-data-dir=$HOME/chromium-client-profile \
      --headless=new \
      --no-sandbox \
      --enable-features=AllowInvalidClientCertForTesting \
      --origin-to-force-client-cert-request=https://your-secure-site.example \
      https://your-secure-site.example
    ```

---

🧠 **Optional: Bypass or trust unknown CA**  
If the certificate chain is not trusted (like UAT/internal), you may need to also import the CA cert into the same NSS profile:

```bash
certutil -A -d sql:~/chromium-client-profile \
         -n "UBS CA" \
         -t "CT,C,C" \
         -a -i ubs-ca.pem
```

`-t "CT,C,C"` tells NSS it's a trusted CA.  
