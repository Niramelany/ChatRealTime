document.addEventListener("DOMContentLoaded", () => {
    const groupChatButton = document.getElementById("groupChatButton");
    const addFriendButton = document.getElementById("addFriendButton");
    const groupChatDialog = document.getElementById("groupChatDialog");
    const addFriendDialog = document.getElementById("addFriendDialog");
    const closeGroupChatDialog = document.getElementById("closeGroupChatDialog");
    const closeAddFriendDialog = document.getElementById("closeAddFriendDialog");
    const createGroupButton = document.getElementById("createGroupButton");
    const addFriendSubmitButton = document.getElementById("addFriendSubmitButton");
    const chatList = document.getElementById("chatList");
    const userNotFound = document.getElementById("userNotFound");

    // Función para abrir un diálogo
    const openDialog = (dialog) => {
        dialog.style.display = "block";
    };

    // Función para cerrar un diálogo
    const closeDialog = (dialog) => {
        dialog.style.display = "none";
    };

    // Abrir diálogo de chat grupal
    groupChatButton.addEventListener("click", () => {
        openDialog(groupChatDialog);
    });

    // Cerrar diálogo de chat grupal
    closeGroupChatDialog.addEventListener("click", () => {
        closeDialog(groupChatDialog);
    });

    // Abrir diálogo de añadir amigo
    addFriendButton.addEventListener("click", () => {
        openDialog(addFriendDialog);
    });

    // Cerrar diálogo de añadir amigo
    closeAddFriendDialog.addEventListener("click", () => {
        closeDialog(addFriendDialog);
    });

    // Crear chat grupal
    createGroupButton.addEventListener("click", () => {
        const groupName = document.getElementById("groupName").value;
        if (groupName) {
            const groupItem = document.createElement("div");
            groupItem.classList.add("chat-item");
            groupItem.innerHTML = `
                <img src="/static/group.png" alt="Group Icon">
            `;
            chatList.appendChild(groupItem);
            closeDialog(groupChatDialog);
        }
    });

    // Añadir amigo
    addFriendSubmitButton.addEventListener("click", () => {
        const friendUsername = document.getElementById("friendUsername").value;
        if (friendUsername) {
            // Simulación de verificación de usuario
            const userExists = Math.random() > 0.5;
            if (userExists) {
                const friendItem = document.createElement("div");
                friendItem.classList.add("chat-item");
                friendItem.innerHTML = `
                    <img src="/static/profile.png" alt="User Icon">
                    <span>${friendUsername}</span>
                `;
                chatList.appendChild(friendItem);
                userNotFound.style.display = "none";
                closeDialog(addFriendDialog);
            } else {
                userNotFound.textContent = "El usuario no existe";
                userNotFound.style.display = "block";
            }
        }
    });
});
