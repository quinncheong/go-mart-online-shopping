import jwt_decode from "jwt-decode"

export const decodeToken = (token) => token ? jwt_decode(token) : null

export const isExpired = ({ exp }) => exp >= Date.now()

export const setToken = (name="cognito-user-jwt", token) => window.localStorage.setItem(name, JSON.stringify(token))

export const getToken = (name="cognito-user-jwt") => {
  const token = JSON.parse(window.localStorage.getItem(name))
  if (!token || isExpired(token)) {
    setToken(name, null)
    console.log("token expired")
    return null
  } else {
    return token
  }
}
