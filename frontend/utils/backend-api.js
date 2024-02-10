import { apiAxios } from "./api-axios"

const axios = apiAxios()

export async function getDailyQuizzes() {
    const url = `/quiz/daily_quizes`

    try {
        const res = await axios.get(url)   
        const json = res.data
        return json['daily_quizes']
    } catch (error) {
        console.error(error)
        return []
    }
};

export async function getQuizAnswer(quiz_id) {
    const url = `/quiz/answer?quiz_id=${quiz_id}`

    try {
        const res = await axios.get(url, {
            withCredentials: true
        })
        return res.data['quiz_answers']
    } catch (error) {
        console.error(error)
        return []
    }
}

export async function getCorrectAnswer(quiz_id) {
    const url = `/quiz/correct_answer?quiz_id=${quiz_id}`

    try {
        const res = await axios.get(url, {
            withCredentials: true
        })
        return res.data["correct_answer"]
    } catch (error) {
        console.error(error)
    }
}

export async function submitAnswer(quiz_id, answer) {
    const url = `/quiz/submit_answer`

    try {
        const res = await axios.post(url, {
            quiz_id,
            answer
        }, {
            withCredentials: true
        })
        const json = res.data
        return json["correct"]
    } catch (error) {
        console.error(error)
    }
};

export async function autoCompleteGameName(query) {
    const url = `/game/auto_complete_name?query=${query}`
    
    try {
        const res = await axios.get(url)
        const json = res.data
        return json['games']
    } catch (error) {
        console.error(error)
        return []
    }
};

export async function authGoogleAuthorize() {
    const url = `/auth/google/authorize`

    try {
        const res = await axios.get(url)
        const json = res.data
        return json["authorization_url"]
    } catch (error) {
        console.error(error)
    }
};

export async function authFacebookAuthorize() {
    const url = `/auth/facebook/authorize`

    try {
        const res = await axios.get(url)
        const json = res.data
        return json["authorization_url"]
    } catch (error) {
        console.error(error)
    }
}

export async function checkLogin() {
    const url = `/auth/check`

    try {
        const res = await axios.post(url, '', {
            validateStatus: status => (status >= 200 && status < 300) || status >= 400,
            withCredentials: true
        })
        
        if (res.status >= 200 && res.status < 300)
            return true
        
    } catch (error) {
        console.error(error)
    }

    return false
};

export async function logout() {
    const url = `/auth/logout`
    return await axios.post(url, '', {withCredentials:true})
};