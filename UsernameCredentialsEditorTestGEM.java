@Test
public void testGetCredentials_WithUsernameOnly() {
  UsernameCredentialsEditor editor = new UsernameCredentialsEditor();
  editor.usernameField.setText("test_user");
  String credentials = editor.getCredentials();
  assertEquals("test_user", credentials);
}

@Test
public void testGetCredentials_WithUsernameAndJwtToken() {
  UsernameCredentialsEditor editor = new UsernameCredentialsEditor();
  editor.usernameField.setText("test_user");
  editor.jwtToken = "your_jwt_token";
  String credentials = editor.getCredentials();
  assertEquals("test_user:your_jwt_token", credentials);
}

@Test
public void testSetCredentials_WithUsernameOnly() {
  UsernameCredentialsEditor editor = new UsernameCredentialsEditor();
  editor.setCredentials("test_user");
  assertEquals("test_user", editor.usernameField.getText());
  assertNull(editor.jwtToken);
}

@Test
public void testSetCredentials_WithUsernameAndJwtToken() {
  UsernameCredentialsEditor editor = new UsernameCredentialsEditor();
  editor.setCredentials("test_user:your_jwt_token");
  assertEquals("test_user", editor.usernameField.getText());
  assertEquals("your_jwt_token", editor.jwtToken);
}

// Placeholder test - Modify based on your secure storage implementation
@Test
public void testSecureStorage_Mocked() {
  // Mock a secure storage library
  SecureStorage mockStorage = Mockito.mock(SecureStorage.class);
  // Simulate storing the JWT token
  editor.jwtToken = "your_jwt_token";
  editor.storeJwtTokenSecurely(mockStorage);
  // Verify that the mock storage method was called with encryption
  Mockito.verify(mockStorage).store(Mockito.anyString(), Mockito.any());
}
