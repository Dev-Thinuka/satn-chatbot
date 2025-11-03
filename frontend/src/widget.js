document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("chat-toggle");
  const closeBtn = document.getElementById("close-chat");
  const container = document.getElementById("chat-widget");
  const fileInput = document.getElementById("file-upload");
  const chatBody = document.querySelector(".chat-body");

  // --- Toggle open/close ---
  toggleBtn.addEventListener("click", () => {
    container.classList.toggle("hidden");
    toggleBtn.style.display = container.classList.contains("hidden") ? "block" : "none";
  });

  closeBtn.addEventListener("click", () => {
    container.classList.add("hidden");
    toggleBtn.style.display = "block";
  });

  // --- File upload handler ---
  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log("File selected:", file.name);
      // Optional: display file preview or send to backend
    }
  });

  // --- Smooth auto-scroll ---
  const smoothScrollToBottom = () => {
    chatBody.scrollTo({
      top: chatBody.scrollHeight,
      behavior: "smooth"
    });
  };

// --- Property Cards Generator ---
function addPropertyCards(properties) {
  const chatBody = document.querySelector('.chat-body');
  const container = document.createElement('div');
  container.className = 'chat-message property-list';
  
  properties.forEach(p => {
    const card = document.createElement('div');
    card.className = 'property-card';
    card.innerHTML = `
      <img src="${p.image}" alt="${p.title}" />
      <div class="property-info">
        <h4>${p.title}</h4>
        <p>${p.description}</p>
        <span class="price">${p.price}</span>
        <button class="property-btn">View Details</button>
      </div>`;
    container.appendChild(card);
  });
  
  function scrollChatToBottom(force = false) {
    const chatBody = document.querySelector('.chat-body');
    const isNearBottom =
      chatBody.scrollHeight - chatBody.scrollTop - chatBody.clientHeight < 100;
    if (isNearBottom || force) {
      chatBody.scrollTop = chatBody.scrollHeight;
    }
  }

  chatBody.appendChild(container);
  smoothScrollToBottom();
}


    

  // ✅ Example demo call:
  // Uncomment below to test auto-property insertion
  /*
  setTimeout(() => {
    addPropertyCards([
      {
        title: "Modern Apartment",
        description: "3 Bed • 2 Bath • 1800 sqft",
        price: "$450,000",
        image: "https://cf.bstatic.com/xdata/images/hotel/max1024x768/619226674.jpg?k=525f03e40bd0cbc7d811a591607baeacc541c82c8556edbf73b88ca662187821&o="
      },
      {
        title: "Luxury Villa",
        description: "5 Bed • 4 Bath • 3200 sqft",
        price: "$1,250,000",
        image: "https://cf.bstatic.com/xdata/images/hotel/max1024x768/619226674.jpg?k=525f03e40bd0cbc7d811a591607baeacc541c82c8556edbf73b88ca662187821&o="
      }
    ]);
  }, 2000);
  */
});
