<template>
    <!-- <div class="chat-container"> -->
      <div class="chat-box">
        <div v-for="(msg, index) in messages" :key="index" :class="['message-wrapper', msg.sender]">
          <img :src="msg.sender === 'bot' ? botAvatar : userAvatar" class="avatar" />
          <div class="message">
            <p class="message-text">{{ msg.text }}</p>
            <button v-if="msg.sender === 'bot' && !msg.helpRequested && msg.text !== 'Hello! How can I assist you today?'" 
              class="no-help-btn" 
              @click="requestItSupport(index)">
              ❌ This didn’t help
            </button>
          </div>
        </div>
      </div>
  
      <!-- 輸入區 -->
      <div class="input-container">
        <input v-model="message" placeholder="Ask something..." @keyup.enter="askChatbot" />
        <button @click="askChatbot">➤</button>
      </div>
    <!-- </div> -->

    
  </template>
  
  <script setup>
  import { ref } from "vue";
  import axios from "axios";
  // **✅ 正確載入圖片**
  import botAvatarImg from "../assets/bot.png";
  import userAvatarImg from "../assets/user.png";
  import { ElMessageBox } from "element-plus";
  import { useRouter } from "vue-router";
  const router = useRouter();
  
  const message = ref("");
  const messages = ref([
    { text: "Hello! How can I assist you today?", sender: "bot", helpRequested: false }
  ]);
  // **✅ 使用 import 的圖片變數**
  const botAvatar = botAvatarImg;
  const userAvatar = userAvatarImg;
  

  
  const askChatbot = async () => {
    if (!message.value.trim()) return;
    messages.value.push({ text: message.value, sender: "user" });
    const userInput = message.value;
    message.value = "";
  
    try {
      const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/chat`, {
        user_id: "user123",
        message: userInput
      });
  
      if (!res.data || !res.data.response) {
        throw new Error("Invalid API response");
      }
  
      messages.value.push({
        text: res.data.response,
        sender: "bot",
        helpRequested: false
      });
  
    } catch (error) {
      console.error("API Error:", error);
      messages.value.push({ text: "Error fetching response.", sender: "bot" });
    }
  };

const requestItSupport = (index) => {
  messages.value[index].helpRequested = true;  // 標記該訊息已請求支援

  ElMessageBox.confirm(
    "This response didn't help. Would you like to contact IT Support?",
    "Need More Help?",
    {
      confirmButtonText: "Yes, Contact IT Support",
      cancelButtonText: "No, I'll try again",
      type: "warning"
    }
  )
    .then(() => {
      // ✅ 用戶選擇 Yes，跳轉到 New Ticket 頁面
      console.log("Redirecting to IT Support page...");
      router.push("/new-ticket");
    })
    .catch(() => {
      // ❌ 用戶選擇 No，留在原頁面
      console.log("User chose not to contact IT Support.");
    });
};

  </script>
  
  <style scoped>
  /* 📌 整個聊天容器 */
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh; /* 滿版高度 */
    width: 100%;
    padding: 20px;
    background: #f5f5f5;
  }
  
  /* 📌 聊天視窗 */
  .chat-box {
    flex-grow: 1;
    overflow-y: auto;
    padding: 15px;
    border-radius: 10px;
    background: white;
    height: 65vh;
    display: flex;
    flex-direction: column;
  }
  
  /* 📌 訊息外框 (包含頭像) */
  .message-wrapper {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  /* 使用者訊息靠右 */
  .user {
    justify-content: flex-end;
  }
  
  /* AI 訊息靠左 */
  .bot {
    justify-content: flex-start;
  }
  
  /* 📌 頭像 */
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 5px;
  }
  
  /* 📌 訊息泡泡 */
  .message {
    max-width: 75%;
    padding: 12px;
    border-radius: 12px;
  }
  
  /* 使用者訊息 (靠右) */
  .user .message {
    background: #007bff;
    color: white;
    text-align: right;
    border-top-right-radius: 0;
  }
  
  /* AI 訊息 (靠左) */
  .bot .message {
    background: #e5e5e5;
    color: black;
    text-align: left;
    border-top-left-radius: 0;
  }
  
  /* 📌 輸入區固定在底部 */
  .input-container {
    display: flex;
    padding: 10px;
    background: white;
    border-top: 1px solid #ddd;
  }
  
  /* 輸入框 */
  input {
    flex-grow: 1;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  /* 送出按鈕 */
  button {
    margin-left: 10px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  /* ❌ This didn’t help 按鈕 */
  .no-help-btn {
    background-color: gray;
    color: white;
    font-size: 12px;
    border: none;
    cursor: pointer;
    padding: 5px;
    margin-top: 5px;
  }
  </style>
  