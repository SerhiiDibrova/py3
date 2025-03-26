

package server.models;

public class Event {
    private int event_id;
    private String name;
    private String date;
    private String status;

    public Event(int event_id, String name, String date, String status) {
        this.event_id = event_id;
        this.name = name;
        this.date = date;
        this.status = status;
    }

    public void update_status(String new_status) {
        this.status = new_status;
    }

    public void update_date(String new_date) {
        this.date = new_date;
    }
}