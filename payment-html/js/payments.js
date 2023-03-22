// to do: loading screen while data is being retrived

let params = new URLSearchParams(document.location.search);
let booking_id = params.get("bookingid");
console.log(booking_id)

const get_booking_info_url = "http://localhost:8000/getbookinginfo";
// const sendVerificationEmailURL = "http://localhost:5103/sendVerificationEmail"

// Vue JS

const orderDetail = Vue.createApp({
    data() {
        return {
            order_id: null,
            user_id: null,
            is_cancelled: 0,
            paid_status: 0,
            booking_date: null,
            price: 0,
            check_in_status: 0,
            payment_id: null,
            email: null,
        }
    },

    methods: {
        getCheckoutDetails() {
            this.order_id = "abc123";
            this.price = parseFloat(23.45).toFixed(2);

            document.getElementById("contentBox").classList.remove("invisible");
            document.getElementById("loadingBox").classList.add("invisible");

            // const detailsResponse =
            //     fetch(get_booking_info_url + "?booking_id=" + booking_id)
            //         .then(detailsResponse => detailsResponse.json())
            //         .then(detailsResponse => {

            //         console.log(detailsResponse);

            //         this.booking_id = detailsResponse.booking_id;
            //         this.flight_id = detailsResponse.flight_id;
            //         this.price = parseFloat(detailsResponse.price).toFixed(2);

            //         // this.email = sessionStorage.getItem("email")
            //         // this.username = sessionStorage.getItem("username")

            //         document.getElementById("contentBox").classList.remove("invisible");
            //         document.getElementById("loadingBox").classList.add("invisible");
            //         })
            //         .catch(error => {
            //             console.log('error message:'+ error);

            //             document.getElementById('loadingText').innerText = `An error has occurred. Error Message: ` + error;
            //         })
                

        },
        // sendVerificationEmail(){
        //     email = this.email
        //     username = this.username
        //     price = this.price
        //     booking_id = this.booking_id

        //     data = {
        //         'email':email,
        //         'username':username,
        //         'price':price,
        //         'booking_id':booking_id
        //     }
            
        //     fetch(sendVerificationEmailURL, data = data)
        //     .then(response => response.json())
        //     .then(response => {

        //         console.log(response);

        //     })
        //     .catch(error => {
        //         error = response["Errors"]["ErrorMessage"]
        //         console.log('error message:'+ error);
        //     })
        // }
    },

    created() {
        this.getCheckoutDetails();
    }
}).mount('#orderDetail')

// const vm = bookingDetail.mount('#bookingDetail');
