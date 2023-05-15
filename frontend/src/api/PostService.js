import axios from "axios";

const url = 'http://localhost:8000/Currencies/currency'

export default class PostService {
    static async getAllCurrency() {
        const response = await axios.get('http://localhost:8000/Currencies/currency')
        return response
    }

    static async getLogin() {
        const response = await axios.post('http://localhost:8000/auth/login')
        return response
    }

//     static async getById(id) {
//         const response = await axios.get(`https://jsonplaceholder.typicode.com/posts/${id}`,)
//         return response
//     }
//
//     static async getCommentsByPostId(id) {
//         const response = await axios.get(`https://jsonplaceholder.typicode.com/posts/${id}/comments`,)
//         return response
//     }
}