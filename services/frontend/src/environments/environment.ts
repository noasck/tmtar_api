import { domain, clientId } from "../../auth-config.json"

export const environment = {
  production: false,
  auth: {
    domain,
    clientId,
    redirectUri: "http://localhost:4200/"
  },
  apiUrl: 'http://localhost:5000/api'
 /* urlAddress: 'http://localhost:4200',
  apiAddress: 'http://localhost:5000/api',*/
  //apiAddress: 'http://37.115.39.187:1337/api'
};
