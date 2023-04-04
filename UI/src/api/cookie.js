import jwt_decode from "jwt-decode"

// retrieve token from cookie -- undefined if there is no cookie for it
export const getCookie = (name) => document.cookie.split("; ").find((cookie) => cookie.startsWith(`${name}=`)).split("=")[1]

// decodes the cookie token -- if cookie is undefined/null, returns null
export const decodeToken = (cookie) => !cookie ? jwt_decode(cookie) : null

// check the token -- true if expired, false otherwise
export const isExpired = ({ exp }) => exp >= Date.now()

export function retrieveCookie(name="idtoken") {
  const cookie = getCookie(name)
  console.log("coded cookie:", cookie)
  const token = decodeToken(cookie)
  console.log("decoded token:", token)
  // if token is undefined or is expired, set undefined and return null
  if (!token || isExpired(token)) {
    document.cookie = `${name}=null`
    return null // return null, do check, if null, do not allow things
  } else {
    return token // return the token for usage
  }
}

export const getRaw = (name="cognito-encoded-jwt") => {
  const rawToken = JSON.parse(window.localStorage.getItem(name))
  if (!rawToken) {
    return null
  } else {
    return rawToken
  }
}
