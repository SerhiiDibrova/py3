

package server.models;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class EventRegistration {
    private int registrationId;
    private int eventId;
    private int patronId;
    private String status;

    public EventRegistration(int registrationId, int eventId, int patronId, String status) {
        this.registrationId = registrationId;
        this.eventId = eventId;
        this.patronId = patronId;
        this.status = status;
    }

    public void updateStatus(String newStatus) {
        this.status = newStatus;
    }

    public ResultSet getEventRegistrationDetails() {
        String query = "SELECT * FROM event_registrations WHERE event_registration_id = ?";
        try (Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/eventdb", "username", "password");
             PreparedStatement pstmt = conn.prepareStatement(query)) {
            pstmt.setInt(1, registrationId);
            return pstmt.executeQuery();
        } catch (SQLException e) {
            return null;
        }
    }
}