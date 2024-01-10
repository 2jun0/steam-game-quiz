import 'dotenv/config'
import path from 'path'

const BACKEND_HOST = process.env.BACKEND_HOST

export async function getDailyQuizes() {
    const url = path.join(BACKEND_HOST, 'quiz/daily_quizes')

    try {
        const res = await fetch(url)   
        const json = await res.json()
        return json['daily_quizes']
    } catch (error) {
        console.error(error)
        return []
    }
}

export function submitAnswer() {

}

export async function autoCompleteGameName(query) {
    const url = path.join(BACKEND_HOST, `game/auto_complete_name?query=${query}`)

    try {
        const res = await fetch(url)
        const json = await res.json()
        return json['games']
    } catch (error) {
        console.error(error)
        return []
    }
}