import { domain, clientId } from "../../auth-config.json"
export const environment = {
  production: true,
  auth: {
    domain,
    clientId,
    redirectUri: "http://localhost:4200/"
  },
  //apiUrl: 'http://37.115.39.187:1337/api'
  apiUrl: 'http://localhost:5000/api'
  
};
//ng serve --configuration production
