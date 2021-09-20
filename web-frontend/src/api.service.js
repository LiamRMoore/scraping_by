const SERVER_URL = "http://0.0.0.0:80/contracts/pcs"

export function perform_get(){
   fetch(SERVER_URL).then(res => res.json())
    .then(
      (result) => {
        console.log(result)
      })
}
