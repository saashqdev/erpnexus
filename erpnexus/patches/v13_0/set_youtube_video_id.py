import saashq

from erpnexus.utilities.doctype.video.video import get_id_from_url


def execute():
	saashq.reload_doc("utilities", "doctype", "video")

	for video in saashq.get_all("Video", fields=["name", "url", "youtube_video_id"]):
		if video.url and not video.youtube_video_id:
			saashq.db.set_value("Video", video.name, "youtube_video_id", get_id_from_url(video.url))
