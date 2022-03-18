import java.io.PrintWriter;
import java.io.StringWriter;
import java.sql.*;

public class DAO {
    private static Connection con;
    private final static String SQL_PHYSICIAN = "SELECT last_name FROM physician WHERE reference_id = ?";
    private final static String SQL_PHYSICIAN_ROLE = "SELECT role FROM physician WHERE reference_id = ?";
    private final static String SQL_CARE_STAFF = "SELECT reference_id FROM carestaff WHERE EHR_id = ? and reference_id = ?";

    public DAO(){
        try {
            Class.forName("org.mariadb.jdbc.Driver");
            con = DriverManager.getConnection("jdbc:mariadb://host.docker.internal/demographics", "root", "");
        } catch (ClassNotFoundException | SQLException e) {
            e.printStackTrace();
        }
    }

    public String getRole(String userId) {
        PreparedStatement stat;
        try {
            stat = con.prepareStatement(SQL_PHYSICIAN_ROLE);
            stat.setString(1, userId);
            ResultSet rs = stat.executeQuery();
            rs.next();
            return rs.getString(1);
        } catch (SQLException e) {
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
        }
        return "";
    }

    public void closeConnection() throws SQLException {
        con.close();
    }

    public boolean isOnTheCareStaff(String ehr_id, String reference_id){
        PreparedStatement stat;
        try {
            stat = con.prepareStatement(SQL_CARE_STAFF);
            stat.setString(1, ehr_id);
            stat.setString(2, reference_id);
            ResultSet rs = stat.executeQuery();
            return rs.next();
        } catch (SQLException e) {
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
        }
        return false;
    }

    public boolean isReceptionist(String userId){
        return getRole(userId).equalsIgnoreCase("receptionist");
    }
}
