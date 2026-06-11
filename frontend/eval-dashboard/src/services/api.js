const BASE_URL="http://localhost/api/v1";

export async function login(username, password){
    const response=await fetch(`${BASE_URL}/auth/login`,
    {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({username, password}),
    });

    if(!response.ok){
        throw new Error("Login Failed");
    }
    return await response.json();


}

export async function getRuns(token){
    const response=await fetch(`${BASE_URL}/runs/`,
        {headers:{"Authorization":`Bearer ${token}`},
    }
    );
    if(!response.ok){
        throw new Error("Failed to fetch runs");
    }
    return await response.json();
}
export async function submitRun(token, prompt, modelOutput) {
    const response = await fetch(`${BASE_URL}/runs/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ 
            experiment_id: 1,
            prompt, 
            model_output: modelOutput,
            model_name: "gemini-pro"
        }),
    });
    if (!response.ok) throw new Error("Failed to submit run");
    return await response.json();
}

export async function triggerEval(token, runId) {
    const response = await fetch(`${BASE_URL}/runs/${runId}/evaluate`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to trigger evaluation");
    return await response.json();
}

export async function getRunById(token, runId) {
    const response = await fetch(`${BASE_URL}/runs/${runId}`, {
        headers: { "Authorization": `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch run");
    return await response.json();
}

export async function logout(token) {
    const response = await fetch(`${BASE_URL}/auth/logout`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Logout failed");
    return await response.json();
}

export async function getMe(token) {
    const response = await fetch(`${BASE_URL}/auth/me`, {
        headers: { "Authorization": `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch user");
    return await response.json();
}