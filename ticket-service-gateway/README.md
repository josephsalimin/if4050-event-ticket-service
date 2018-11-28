# TicketX
**TicketX** is a web service that provides ticket for events. **TicketX** uses *Spyne* as the SOAP server, and Camunda BPM as the business process engine.

## Usage
**TicketX** can be used in three ways by other services:
  
  1. Creating event for partners (event organizer)
  2. Book events.
  3. Pay the booked event.
  4. Cancel the booking that has been booked by the user.

## API
The definition of these complex models can be seen in the WSDL. You have to be using the ITB network or using ITB VPN to access it. 


```CreateEvent(EventTicketRequest): EventTicketResp```

The *EventTicketRequest* consists of the event and the list of sections of the event. This method will create a new event based on the provided data sent to the request. 
[WSDL](http://167.205.35.225:8000/?create_event?wsdl)


```BookEvent(BookEventRequest): BookEventResp```

The *BookEventRequest* consists of the *user id* and the list of sections that wants to be booked. This method will book the sections of the event with the user specified by the *user id* as the booker. This method will return the *order id* corresponding to the booked sections/event.
[WSDL](http://167.205.35.225:8000/?book_event?wsdl)


```CancelOrder(CancelOrderRequest): CancelOrderResp```

The *CancelOrderRequest* consists of an *order id*. This *order id* is the specifier for the order (booking) that want to be cancelled. This method will cancel the booking with the given *order id*.
[WSDL](http://167.205.35.225:8000/?cancel_order?wsdl)


```OrderPayment(OrderPaymentRequest): OrderPaymentResp```

The *OrderPaymentRequest* consists of *user id*, *order id*, and the Camunda *instance id*. These data will be sent to make the payment of the order that is specified by the given data.
[WSDL](http://167.205.35.225:8000/?book_event?wsdl)

All of these *API* request type will consists of a callback type to specify the type of callback that the service will send.
