import jwt_decode from "jwt-decode"

export const decodeToken = (token) => token ? jwt_decode(token) : null

export const isExpired = (token) => token ? (token.exp * 1000) < Date.now() : false // false because even if null, will return itself later (as null)

export const setToken = (name="cognito-user-jwt", token) => window.localStorage.setItem(name, JSON.stringify(token))

export const getToken = (name="cognito-user-jwt") => {
  const token = JSON.parse(window.localStorage.getItem(name))
  if (isExpired(token)) {
    setToken(name, null)
    if (name === "cognito-user-jwt") {
      setToken("cognito-encoded-jwt", null)
    }
    console.log("token expired")
    return null
  } else {
    return token
  }
}

export const getRaw = (name="cognito-encoded-jwt") => JSON.parse(window.localStorage.getItem(name))
