import jwt_decode from "jwt-decode"

// retrieve token from cookie -- undefined if there is no cookie for it
export const getCookie = (name) => document.cookie.split("; ").find((cookie) => cookie.startsWith(`${name}=`)).split("=")[1]

// decodes the cookie token -- if cookie is undefined, returns undefined
export const decodeToken = (cookie) => cookie ? jwt_decode(cookie) : undefined

// check the token -- true if token not expired, false if expired
export const checkToken = ({ exp }) => exp < Date.now()
