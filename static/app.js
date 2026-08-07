// static/app.js

const form = document.getElementById("booklet-form");
const button = document.getElementById("generate-button");
const status = document.getElementById("status");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    button.disabled = true;
    status.textContent = "Generating booklet...";

    const requestBody = {
        title: document.getElementById("title").value,
        zpub: document.getElementById("zpub").value.trim(),
        lightning_address:
            document.getElementById("lightning_address").value.trim(),
        num_addresses:
            Number(document.getElementById("num_addresses").value),
    };

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText);
        }

        const pdfBlob = await response.blob();

        const downloadUrl = URL.createObjectURL(pdfBlob);

        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = "bitcoin-deposit-booklet.pdf";

        document.body.appendChild(link);
        link.click();
        link.remove();

        URL.revokeObjectURL(downloadUrl);

        status.textContent = "Booklet generated.";

    } catch (error) {
        console.error(error);
        status.textContent = "Something went wrong generating the booklet.";
    } finally {
        button.disabled = false;
    }
});
