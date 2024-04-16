import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class UsernameCredentialsEditorTest {
    private UsernameCredentialsEditor editor;

    @Before
    public void setUp() {
        editor = new UsernameCredentialsEditor();
    }

    @Test
    public void testGetCredentials_NoToken() {
        editor.usernameField.setText("username");
        assertEquals("username", editor.getCredentials());
    }

    @Test
    public void testGetCredentials_WithToken() {
        editor.usernameField.setText("username");
        editor.jwtToken = "jwtToken";
        assertEquals("username:jwtToken", editor.getCredentials());
    }

    @Test
    public void testGetViewableCredentials_NoToken() {
        editor.usernameField.setText("username");
        assertEquals("username", editor.getViewableCredentials());
    }

    @Test
    public void testGetViewableCredentials_WithToken() {
        editor.usernameField.setText("username");
        editor.jwtToken = "jwtToken";
        assertEquals("username:*****", editor.getViewableCredentials());
    }

    @Test
    public void testSetCredentials_NoToken() {
        editor.setCredentials("username");
        assertEquals("username", editor.usernameField.getText());
        assertNull(editor.jwtToken);
    }

    @Test
    public void testSetCredentials_WithToken() {
        editor.setCredentials("username:jwtToken");
        assertEquals("username", editor.usernameField.getText());
        assertEquals("jwtToken", editor.jwtToken);
    }

    // You can write more tests to cover edge cases and exception handling
}
