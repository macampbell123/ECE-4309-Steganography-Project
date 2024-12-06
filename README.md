The program provides a secure way to encrypt and decrypt user-entered text while ensuring privacy through input masking. As users type, their input is masked with 'X' to protect sensitive data. Basic editing is supported, allowing users to delete characters using the backspace key. The input text is then encrypted using the AES-GCM encryption algorithm, with a password-derived key for secure encryption. The encrypted result is encoded in Base64 to make it portable. AES-GCM (Advanced Encryption Standard with Galois/Counter Mode) is a symmetric cryptographic algorithm that offers data integrity and authenticated encryption, widely used in protocols like MACsec, ANSI Fibre Channel Security Protocols, and IEEE 1619 group for securing data-at-rest.

To demonstrate, I typed the text "Marcus Campbell," which was masked with the letter X as I typed. The system then displayed the encrypted version of the text. Next, I was prompted to enter the password. After inputting "Marcus1," the system successfully decrypted the text, revealing "Marcus Campbell.
![image](https://github.com/user-attachments/assets/60437965-4a7a-4c61-988d-2cad7be7dac2)


In a more realistic scenario, to deceive someone who doesn't know the key, if they enter the wrong one, the system will display a fake decrypted text that matches the number of words in the original text. This creates the illusion that the decryption was successful, even though the incorrect key was used.
![image](https://github.com/user-attachments/assets/3052c3ef-53d7-47ab-8ee2-74aa63aca1d9)
