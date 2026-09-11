/* =========================================================
   VELORA STYLE 14
   Main Website JavaScript
========================================================= */


/* =========================================================
   PRODUCT DATA
========================================================= */

const products = window.VELORA_PRODUCTS || [];

const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const typingIndicator = document.getElementById("typingIndicator");

const aiFloatingButton = document.getElementById("aiFloatingButton");
const aiChatWindow = document.getElementById("aiChatWindow");
const closeAiChat = document.getElementById("closeAiChat");

const productModal = document.getElementById("productModal");
const closeProductModal = document.getElementById("closeProductModal");

const searchButton = document.getElementById("searchButton");
const searchOverlay = document.getElementById("searchOverlay");
const closeSearch = document.getElementById("closeSearch");
const productSearch = document.getElementById("productSearch");
const searchSubmit = document.getElementById("searchSubmit");
const searchResults = document.getElementById("searchResults");

const mobileMenuButton = document.getElementById("mobileMenuButton");
const mainNav = document.getElementById("mainNav");

const productGrid = document.getElementById("productGrid");
const categoryTabs = document.querySelectorAll(".category-tab");

let currentProduct = null;


/* =========================================================
   HELPERS
========================================================= */

function formatPrice(price) {
    return "₹" + Number(price).toLocaleString("en-IN");
}


function escapeHTML(value) {

    const div = document.createElement("div");

    div.textContent = String(value ?? "");

    return div.innerHTML;
}


function scrollChatBottom() {

    if (!chatBox) return;

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =========================================================
   MOBILE MENU
========================================================= */

if (mobileMenuButton) {

    mobileMenuButton.addEventListener("click", () => {

        mainNav.classList.toggle("open");

        const isOpen = mainNav.classList.contains("open");

        mobileMenuButton.textContent = isOpen ? "×" : "☰";

    });
}


document.querySelectorAll(".nav-link").forEach(link => {

    link.addEventListener("click", () => {

        mainNav.classList.remove("open");

        if (mobileMenuButton) {
            mobileMenuButton.textContent = "☰";
        }

    });

});


/* =========================================================
   NAV ACTIVE STATE
========================================================= */

const sections = document.querySelectorAll("main section[id]");

const observer = new IntersectionObserver(
    entries => {

        entries.forEach(entry => {

            if (!entry.isIntersecting) return;

            const id = entry.target.id;

            document.querySelectorAll(".nav-link").forEach(link => {

                link.classList.toggle(
                    "active",
                    link.getAttribute("href") === "#" + id
                );

            });

        });

    },
    {
        rootMargin: "-30% 0px -60% 0px"
    }
);


sections.forEach(section => observer.observe(section));


/* =========================================================
   CATEGORY FILTERS
========================================================= */

function filterProducts(category) {

    if (!productGrid) return;

    const cards = productGrid.querySelectorAll(".product-card");

    cards.forEach(card => {

        const cardCategory = card.dataset.category;

        const show =
            category === "all" ||
            cardCategory === category;

        if (show) {

            card.classList.remove("hidden");

            card.classList.remove("fade-in");

            void card.offsetWidth;

            card.classList.add("fade-in");

        } else {

            card.classList.add("hidden");

        }

    });

}


categoryTabs.forEach(tab => {

    tab.addEventListener("click", () => {

        categoryTabs.forEach(item => {
            item.classList.remove("active");
        });

        tab.classList.add("active");

        const category = tab.dataset.category;

        filterProducts(category);

        document
            .getElementById("new-arrivals")
            ?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

    });

});


/* =========================================================
   TREND / MOOD FILTERS
========================================================= */

function filterByOccasion(occasion) {

    const cards = productGrid?.querySelectorAll(".product-card");

    if (!cards) return;

    cards.forEach(card => {

        const id = Number(card.dataset.productId);

        const product = products.find(item => item.id === id);

        if (!product) return;

        const show =
            product.occasion.toLowerCase() ===
            occasion.toLowerCase();

        card.classList.toggle("hidden", !show);

    });

    categoryTabs.forEach(tab => {
        tab.classList.remove("active");
    });

}


document.querySelectorAll(".mood-card").forEach(card => {

    card.addEventListener("click", () => {

        const mood = card.dataset.mood;

        filterByOccasion(mood);

        document
            .getElementById("new-arrivals")
            ?.scrollIntoView({
                behavior: "smooth"
            });

    });

});


document.querySelectorAll(".trend-link").forEach(button => {

    button.addEventListener("click", () => {

        const category = button.dataset.categoryFilter;

        if (!category) return;

        categoryTabs.forEach(tab => {

            tab.classList.toggle(
                "active",
                tab.dataset.category === category
            );

        });

        filterProducts(category);

        document
            .getElementById("new-arrivals")
            ?.scrollIntoView({
                behavior: "smooth"
            });

    });

});


/* =========================================================
   WISHLIST
========================================================= */

document.querySelectorAll(".product-wishlist").forEach(button => {

    button.addEventListener("click", event => {

        event.preventDefault();

        button.classList.toggle("liked");

        button.textContent =
            button.classList.contains("liked")
                ? "♥"
                : "♡";

    });

});


/* =========================================================
   PRODUCT MODAL
========================================================= */

function openProductModal(productId) {

    const product = products.find(
        item => Number(item.id) === Number(productId)
    );

    if (!product || !productModal) return;

    currentProduct = product;

    const image = document.getElementById("modalProductImage");
    const category = document.getElementById("modalProductCategory");
    const name = document.getElementById("modalProductName");
    const price = document.getElementById("modalProductPrice");
    const description = document.getElementById("modalProductDescription");
    const sizes = document.getElementById("modalSizes");
    const colors = document.getElementById("modalColors");
    const occasion = document.getElementById("modalOccasion");

    image.src = product.image;
    image.alt = product.name;

    category.textContent = product.category.toUpperCase();

    name.textContent = product.name;

    price.textContent = formatPrice(product.price);

    description.textContent = product.description;

    colors.textContent = product.colors.join(", ");

    occasion.textContent = product.occasion;

    sizes.innerHTML = "";

    product.sizes.forEach(size => {

        const button = document.createElement("button");

        button.className = "size-option";

        button.type = "button";

        button.textContent = size;

        button.addEventListener("click", () => {

            sizes
                .querySelectorAll(".size-option")
                .forEach(item => {
                    item.classList.remove("selected");
                });

            button.classList.add("selected");

        });

        sizes.appendChild(button);

    });

    productModal.classList.add("open");

    document.body.classList.add("no-scroll");

}


function closeModal() {

    if (!productModal) return;

    productModal.classList.remove("open");

    document.body.classList.remove("no-scroll");

}


document.querySelectorAll(".quick-view").forEach(button => {

    button.addEventListener("click", () => {

        openProductModal(button.dataset.productId);

    });

});


if (closeProductModal) {
    closeProductModal.addEventListener("click", closeModal);
}


if (productModal) {

    productModal.addEventListener("click", event => {

        if (event.target === productModal) {
            closeModal();
        }

    });

}


/* =========================================================
   INSTAGRAM ORDER
========================================================= */

const modalOrderButton =
    document.getElementById("modalOrderButton");


if (modalOrderButton) {

    modalOrderButton.addEventListener("click", () => {

        if (!currentProduct) return;

        const message =
            `Hi Velora Style 14! I want to order "${currentProduct.name}" for ${formatPrice(currentProduct.price)}.`;

        const instagramUrl =
            "https://instagram.com/velora_style14";

        window.open(
            instagramUrl,
            "_blank",
            "noopener,noreferrer"
        );

        closeModal();

    });

}


/* =========================================================
   SEARCH
========================================================= */

function openSearch() {

    searchOverlay?.classList.add("open");

    setTimeout(() => {
        productSearch?.focus();
    }, 100);

    document.body.classList.add("no-scroll");

}


function closeSearchOverlay() {

    searchOverlay?.classList.remove("open");

    document.body.classList.remove("no-scroll");

}


if (searchButton) {
    searchButton.addEventListener("click", openSearch);
}


if (closeSearch) {
    closeSearch.addEventListener(
        "click",
        closeSearchOverlay
    );
}


if (searchOverlay) {

    searchOverlay.addEventListener("click", event => {

        if (event.target === searchOverlay) {
            closeSearchOverlay();
        }

    });

}


function performSearch() {

    const query =
        productSearch?.value.trim().toLowerCase();

    if (!searchResults) return;

    searchResults.innerHTML = "";

    if (!query) {

        searchResults.innerHTML = `
            <p style="font-size:12px;color:#77716a;">
                Try searching for dresses, jeans, shirts or party wear.
            </p>
        `;

        return;
    }

    const matches = products.filter(product => {

        const searchable = [
            product.name,
            product.category,
            product.occasion,
            product.description,
            ...(product.colors || [])
        ]
            .join(" ")
            .toLowerCase();

        return searchable.includes(query);

    });


    if (!matches.length) {

        searchResults.innerHTML = `
            <p style="font-size:12px;color:#77716a;">
                No products found for "${escapeHTML(query)}".
            </p>
        `;

        return;
    }


    matches.forEach(product => {

        const result = document.createElement("button");

        result.type = "button";

        result.className = "search-result";

        result.innerHTML = `
            <span>${escapeHTML(product.name)}</span>
            <strong>${formatPrice(product.price)}</strong>
        `;

        result.addEventListener("click", () => {

            closeSearchOverlay();

            openProductModal(product.id);

        });

        searchResults.appendChild(result);

    });

}


if (searchSubmit) {
    searchSubmit.addEventListener(
        "click",
        performSearch
    );
}


if (productSearch) {

    productSearch.addEventListener("keydown", event => {

        if (event.key === "Enter") {

            event.preventDefault();

            performSearch();

        }

    });

    productSearch.addEventListener(
        "input",
        performSearch
    );

}


/* =========================================================
   AI CHAT — OPEN / CLOSE
========================================================= */

function openAiChat() {

    if (!aiChatWindow) return;

    aiChatWindow.classList.add("open");

    aiChatWindow.setAttribute(
        "aria-hidden",
        "false"
    );

    setTimeout(() => {
        userInput?.focus();
        scrollChatBottom();
    }, 150);

}


function closeAiChatWindow() {

    if (!aiChatWindow) return;

    aiChatWindow.classList.remove("open");

    aiChatWindow.setAttribute(
        "aria-hidden",
        "true"
    );

}


if (aiFloatingButton) {

    aiFloatingButton.addEventListener(
        "click",
        openAiChat
    );

}


if (closeAiChat) {

    closeAiChat.addEventListener(
        "click",
        closeAiChatWindow
    );

}


document
    .getElementById("openAiFromBanner")
    ?.addEventListener(
        "click",
        openAiChat
    );


document
    .getElementById("footerAiButton")
    ?.addEventListener(
        "click",
        event => {

            event.preventDefault();

            openAiChat();

        }
    );


/* =========================================================
   ADD CHAT MESSAGE
========================================================= */

function addUserMessage(text) {

    const wrapper =
        document.createElement("div");

    wrapper.className = "ai-user-message";

    const bubble =
        document.createElement("div");

    bubble.className = "chat-bubble";

    bubble.textContent = text;

    wrapper.appendChild(bubble);

    chatBox.appendChild(wrapper);

    scrollChatBottom();

}


function addBotMessage(text) {

    const wrapper =
        document.createElement("div");

    wrapper.className = "ai-bot-message";

    const avatar =
        document.createElement("div");

    avatar.className = "chat-avatar";

    avatar.textContent = "✦";

    const bubble =
        document.createElement("div");

    bubble.className = "chat-bubble";

    const strong =
        document.createElement("strong");

    strong.textContent = "Velora AI";

    const paragraph =
        document.createElement("p");

    /*
       textContent keeps the AI response safe.
       Convert line breaks into visual spacing without
       using unsafe HTML.
    */

    const safeText =
        String(text ?? "Something went wrong.");

    paragraph.textContent = safeText;

    bubble.appendChild(strong);

    bubble.appendChild(paragraph);

    wrapper.appendChild(avatar);

    wrapper.appendChild(bubble);

    chatBox.appendChild(wrapper);

    scrollChatBottom();

}


/* =========================================================
   TYPING INDICATOR
========================================================= */

function showTyping() {

    if (!typingIndicator) return;

    typingIndicator.style.display = "flex";

    scrollChatBottom();

}


function hideTyping() {

    if (!typingIndicator) return;

    typingIndicator.style.display = "none";

}


/* =========================================================
   CHAT INPUT STATE
========================================================= */

function disableChatInput() {

    if (!sendBtn || !userInput) return;

    sendBtn.disabled = true;

    userInput.disabled = true;

}


function enableChatInput() {

    if (!sendBtn || !userInput) return;

    sendBtn.disabled = false;

    userInput.disabled = false;

    userInput.focus();

}


/* =========================================================
   SEND MESSAGE TO FLASK
========================================================= */

async function sendMessage() {

    if (!userInput || !chatBox) return;

    const text =
        userInput.value.trim();

    if (!text) return;


    addUserMessage(text);

    userInput.value = "";

    userInput.style.height = "40px";

    disableChatInput();

    showTyping();


    try {

        const response =
            await fetch("/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text
                })

            });


        let data;

        try {

            data = await response.json();

        } catch {

            data = {
                success: false,
                response: "The server returned an invalid response."
            };

        }


        hideTyping();

        enableChatInput();


        if (response.ok && data.success) {

            addBotMessage(data.response);

        } else {

            addBotMessage(
                data.response ||
                "Our AI Stylist is temporarily unavailable. Please try again."
            );

        }

    } catch (error) {

        console.error(
            "Velora AI error:",
            error
        );

        hideTyping();

        enableChatInput();

        addBotMessage(
            "I couldn't connect to Velora AI right now. Please check that the website server is running and try again."
        );

    }

}


/* =========================================================
   SEND BUTTON
========================================================= */

if (sendBtn) {

    sendBtn.addEventListener(
        "click",
        sendMessage
    );

}


/* =========================================================
   ENTER TO SEND
========================================================= */

if (userInput) {

    userInput.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();

            }

        }
    );

}


/* =========================================================
   TEXTAREA AUTO RESIZE
========================================================= */

if (userInput) {

    userInput.addEventListener(
        "input",
        function () {

            this.style.height = "auto";

            this.style.height =
                Math.min(
                    this.scrollHeight,
                    80
                ) + "px";

        }
    );

}


/* =========================================================
   AI SUGGESTION CHIPS
========================================================= */

document
    .querySelectorAll(".suggestion-chip")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                if (!userInput) return;

                userInput.value =
                    button.textContent.trim();

                sendMessage();

            }
        );

    });


/* =========================================================
   ESCAPE KEY
========================================================= */

document.addEventListener(
    "keydown",
    event => {

        if (event.key !== "Escape") return;

        closeSearchOverlay();

        closeModal();

        closeAiChatWindow();

        mainNav?.classList.remove("open");

        if (mobileMenuButton) {
            mobileMenuButton.textContent = "☰";
        }

    }
);


/* =========================================================
   FOOTER HELP SHORTCUTS
========================================================= */

document
    .getElementById("footerSizeGuide")
    ?.addEventListener(
        "click",
        event => {

            event.preventDefault();

            openAiChat();

            setTimeout(() => {

                if (!userInput) return;

                userInput.value =
                    "Help me choose a size";

                sendMessage();

            }, 200);

        }
    );


document
    .getElementById("footerDelivery")
    ?.addEventListener(
        "click",
        event => {

            event.preventDefault();

            openAiChat();

            setTimeout(() => {

                if (!userInput) return;

                userInput.value =
                    "Tell me about delivery";

                sendMessage();

            }, 200);

        }
    );


document
    .getElementById("footerExchange")
    ?.addEventListener(
        "click",
        event => {

            event.preventDefault();

            openAiChat();

            setTimeout(() => {

                if (!userInput) return;

                userInput.value =
                    "Tell me about exchange";

                sendMessage();

            }, 200);

        }
    );


/* =========================================================
   BAG BUTTON
========================================================= */

document
    .querySelector(".bag-button")
    ?.addEventListener(
        "click",
        () => {

            openAiChat();

            setTimeout(() => {

                addBotMessage(
                    "Your shopping bag is ready for future purchases ✨ For now, you can select any product and order it through our Instagram DM."
                );

            }, 200);

        }
    );


/* =========================================================
   INITIAL PRODUCT STATE
========================================================= */

filterProducts("all");


/* =========================================================
   INITIAL CHAT SCROLL
========================================================= */

setTimeout(() => {

    scrollChatBottom();

}, 250);


/* =========================================================
   CONSOLE CHECK
========================================================= */

console.log(
    `Velora Style 14 loaded — ${products.length} products available.`
);