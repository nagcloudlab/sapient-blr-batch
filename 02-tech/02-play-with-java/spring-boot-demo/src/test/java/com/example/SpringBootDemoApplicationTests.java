package com.example;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class SpringBootDemoApplicationTests {

	@Autowired
	private MockMvc mockMvc;

	@Test
	void shouldCreateUpdateReadAndDeleteTodo() throws Exception {
		String createPayload = """
				{
					\"title\": \"Buy milk\",
					\"description\": \"From the market\",
					\"completed\": false
				}
			""";

		mockMvc.perform(post("/todos")
				.contentType(MediaType.APPLICATION_JSON)
				.content(createPayload))
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.title").value("Buy milk"));

		mockMvc.perform(get("/todos"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$[0].title").value("Buy milk"));

		String updatePayload = """
				{
					\"title\": \"Buy milk\",
					\"description\": \"From the market\",
					\"completed\": true
				}
			""";

		mockMvc.perform(put("/todos/1")
				.contentType(MediaType.APPLICATION_JSON)
				.content(updatePayload))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.completed").value(true));

		mockMvc.perform(delete("/todos/1"))
				.andExpect(status().isNoContent());

		mockMvc.perform(get("/todos/1"))
				.andExpect(status().isNotFound());
	}
}
