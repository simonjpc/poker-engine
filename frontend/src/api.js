import axios from 'axios';

const API_URL = "http://localhost:4000";

export async function startGame() {
    const res = await fetch(`${API_URL}/start_game`, {
        method: "POST",
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to start game: ${res.status} ${errorText}`);
    }

    return res.json();
}

export const fetchGameState = async () => {
    const response = await axios.get(`${API_URL}/game_state`);
    return response.data;
};

export const sendAction = async (player, action, amount = 0) => {
    await axios.post(`${API_URL}/action`, { player, action, amount });
};

export const startNextHand = async () => {
    await axios.post(`${API_URL}/next_hand`);
};

export async function sendGameConfig(config) {
    const res = await fetch(`${API_URL}/game_config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
    });
    return await res.json();
}

export async function resetGame() {
    const res = await fetch(`${API_URL}/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    return res.json();
  }