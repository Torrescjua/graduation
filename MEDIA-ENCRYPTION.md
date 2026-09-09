# Encrypted media deployment

`fotos.enc` is the encrypted archive of the published images and videos. It is
stored with Git LFS because it is larger than GitHub's regular file limit. The
GitHub Pages workflow downloads and decrypts it only while building the
deployment artifact.

## Initial setup

1. Ensure Git for Windows or OpenSSL is installed locally.
2. Run `powershell -ExecutionPolicy Bypass -File tools/protect-media.ps1` and
   enter a strong passphrase when PowerShell asks for it.
3. In the GitHub repository, add an Actions secret named `MEDIA_PASSPHRASE`
   containing exactly that passphrase.
4. Remove the already tracked plaintext media without deleting the local files:
   `git rm --cached -r fotos`
5. Restore the tracked placeholder: `git add fotos/.mantener-esta-carpeta`.
6. Commit `fotos.enc`, `.gitignore`, the workflow, the script, and this guide.

## Updating media

After adding, replacing, or removing files in `fotos/`, run the script again
with the same passphrase and commit the updated `fotos.enc`.

The deployed GitHub Pages site still serves decrypted photos and videos to its
visitors. This setup prevents plaintext media from being present in future
repository commits; it does not make a public deployed site private.

Existing Git history still contains the original plaintext files. Use GitHub's
documentation for removing sensitive data from a repository if that history
must also be purged.