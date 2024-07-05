export class HttpResponseError extends Error {
    constructor(status, message) {
        super(message);
        this.name = "HttpResponseError";
        this.status = status;
    }
}