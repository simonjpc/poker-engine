import axios from 'axios';

const API_URL = "http://127.0.0.1:5000";

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
