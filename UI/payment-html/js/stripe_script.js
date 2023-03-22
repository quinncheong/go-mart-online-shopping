var stripe = Stripe(
	"pk_test_51KegmTDlqIwRfGLS8skxZOKRQ86IEqZ2uEeZET5H6gWVP1J92gF5qK5xcAmAH2DlX1IbpnRCk445erHe6yKzrBSz00LHcNYTrM"
);

var elements = stripe.elements();

const payment_url =
	"http://strip-loadb-tauc5vcf95y1-7b686638c7ffd343.elb.us-east-1.amazonaws.com:8000";
// const payment_url = "http://localhost:8000"

// Set up Stripe.js and Elements to use in checkout form
var style = {
	base: {
		iconColor: "#202020",
		color: "#202020",
		fontWeight: "500",
		fontFamily: "Roboto, Open Sans, Segoe UI, sans-serif",
		fontSize: "16px",
		fontSmoothing: "antialiased",
		":-webkit-autofill": {
			color: "#202020",
		},
		"::placeholder": {
			color: "#202020",
		},
	},
	invalid: {
		iconColor: "#B22222",
		color: "#B22222",
	},
};

var cardElement = elements.create("card", {
	hidePostalCode: true,
	style: style,
});
cardElement.mount("#card-element");

var form = document.getElementById("payment-form");

form.addEventListener("submit", function (event) {
	// We don't want to let default form submission happen here,
	// which would refresh the page.
	event.preventDefault();

	submitEle = document.getElementById("submit");
	submitEle.classList.add("disabled");

	errorEle = document.getElementById("error-box");
	errorEle.classList.add("invisible");

	submitSpinnerEle = document.getElementById("button-text");
	submitSpinnerEle.innerText = "Processing payment...";

	stripe
		.createPaymentMethod({
			type: "card",
			card: cardElement,
			billing_details: {
				// Include any additional collected billing details.
			},
		})
		.then(stripePaymentMethodHandler);
});

function stripePaymentMethodHandler(result) {
	if (result.error) {
		// Show error in payment form
		errorEle = document.getElementById("error-box");
		errorEle.innerText = result.error.message;
		errorEle.classList.remove("invisible");

		console.log(result.error);

		submitEle = document.getElementById("submit");
		submitEle.classList.remove("disabled");

		submitSpinnerEle = document.getElementById("button-text");
		submitSpinnerEle.innerText = "Pay Now";
	} else {
		// Otherwise send paymentMethod.id to your server (see Step 4)
		fetch(payment_url + "/new_payment", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				payment_method_id: result.paymentMethod.id,
				order_id: orderDetail.order_id,
				amount: orderDetail.price,
				// email : sessionStorage.getItem("email"),
				// username : sessionStorage.getItem("username"),
			}),
		}).then(function (result) {
			// Handle server response (see Step 4)
			result.json().then(function (json) {
				handleServerResponse(json);
			});
		});
	}
}

function handleServerResponse(response) {
	if (response.error) {
		console.log(response.error);
		// Show error from server on payment form
		errorEle = document.getElementById("error-box");
		errorEle.innerText = response.error;
		errorEle.classList.remove("invisible");

		submitSpinnerEle = document.getElementById("button-text");
		submitSpinnerEle.innerText = "Pay Now";

		submitEle = document.getElementById("submit");
		submitEle.classList.remove("disabled");

		console.log(response.error);
	} else if (response.requires_action) {
		// Use Stripe.js to handle required card action
		stripe
			.handleCardAction(response.payment_intent_client_secret)
			.then(handleStripeJsResult);
	} else {
		// Show success message
		console.log(response);

		// bugged - needs condition if server fails
		// alert("Payment Success!");
		// window.location.replace("./success.html");
	}
}

function handleStripeJsResult(result) {
	if (result.error) {
		// Show error in payment form
		console.log(result);
		errorEle = document.getElementById("error-box");
		errorEle.innerText = result.error;

		if ("code" in result.error) {
			errorEle.innerText = result.error.message;
		}

		errorEle.classList.remove("invisible");
		submitEle.classList.remove("disabled");

		submitSpinnerEle = document.getElementById("button-text");
		submitSpinnerEle.innerText = "Pay Now";

		console.log(result.error);
	} else {
		// The card action has been handled
		// The PaymentIntent can be confirmed again on the server
		fetch(payment_url + "/new_payment", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				payment_intent_id: result.paymentIntent.id,
				// email : sessionStorage.getItem("email"),
				// username : sessionStorage.getItem("username"),
				order_id: orderDetail.order_id,
			}),
		})
			.then(function (confirmResult) {
				return confirmResult.json();
			})
			.then(handleServerResponse);
	}
}
