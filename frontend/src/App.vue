<template>
  <div class="chat-container">
    <h2>AI IT Support Chatbot</h2>
    <div class="chat-box">
      <div v-for="(msg, index) in chatHistory" :key="index" :class="msg.role">
        <strong v-if="msg.role === 'user'">You:</strong>
        <strong v-if="msg.role === 'bot'">Bot:</strong>
        <p>{{ msg.message }}</p>
      </div>
    </div>
    <input v-model="userMessage" placeholder="Ask something..." @keyup.enter="askChatbot" />
    <button @click="askChatbot">Send</button>

    <!-- IT Support 按鈕 -->
    <button v-if="showSupportButton" @click="createTicket">Contact IT Support</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
const userMessage = ref("");
const chatHistory = ref([]);
const showSupportButton = ref(false);
const userId = "user123"; // 模擬用戶 ID

const askChatbot = async () => {
  if (!userMessage.value.trim()) return;

  // 添加用戶的訊息到聊天紀錄
  chatHistory.value.push({ role: "user", message: userMessage.value });

  try {
    const res = await axios.post(`${apiBaseUrl}/chat`, {
      user_id: userId,
      message: userMessage.value
    });

    // 添加 AI 回覆到聊天紀錄
    chatHistory.value.push({ role: "bot", message: res.data.response });

    // 如果 AI 回應建議聯繫 IT Support，則顯示按鈕
    showSupportButton.value = res.data.suggest_ticket;
  } catch (error) {
    console.error("Error fetching response:", error);
    chatHistory.value.push({ role: "bot", message: "Error fetching response." });
  }

  userMessage.value = ""; // 清空輸入框
};

const createTicket = async () => {
  try {
    const res = await axios.post(`${apiBaseUrl}/ticket`, {
      user_id: userId,
      issue: "User unable to resolve issue via chatbot."
    });

    chatHistory.value.push({ role: "bot", message: `Ticket submitted! Ticket ID: ${res.data.ticket_id}` });
    showSupportButton.value = false; // 提交報修後隱藏按鈕
  } catch (error) {
    console.error("Error submitting ticket:", error);
    chatHistory.value.push({ role: "bot", message: "Failed to submit ticket." });
  }
};
</script>

<style>
.chat-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.chat-box {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  background: #f9f9f9;
}

.user {
  text-align: right;
  color: blue;
}

.bot {
  text-align: left;
  color: green;
}

input {
  width: 80%;
  padding: 10px;
  margin-bottom: 10px;
}

button {
  padding: 10px 15px;
  margin: 5px;
  background-color: blue;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
