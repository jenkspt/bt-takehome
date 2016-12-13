### [Post fields description](http://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede)
(source is 7 years old so may be outdated)

* Id
* PostTypeId (listed in the PostTypes table)
		1. Question
		2. Answer
		3. Orphaned tag wiki
		4. Tag wiki excerpt
		5. Tag wiki
		6. Moderator nomination
		7. "Wiki placeholder" (seems to only be the election description)
		8. Privilege wiki
* AcceptedAnswerId (only present if PostTypeId is 1)
* ParentID (only present if PostTypeId is 2)
* CreationDate
* DeletionDate (only non-null for the SEDE PostsWithDeleted table. Deleted posts are not present on Posts. Column not present on data dump.)
* Score
* ViewCount (nullable)
* Body (as rendered HTML, not Markdown)
* OwnerUserId (only present if user has not been deleted; always -1 for tag wiki entries, i.e. the community user owns them)
* OwnerDisplayName (nullable)
* LastEditorUserId (nullable)
* LastEditorDisplayName (nullable)
* LastEditDate="2009-03-05T22:28:34.823" - the date and time of the most recent edit to the post (nullable)
* LastActivityDate="2009-03-11T12:51:01.480" - the date and time of the most recent activity on the post. For a question, this could be the post being edited, a new answer was posted, a bounty was started, etc.
* Title (nullable)
* Tags (nullable)
* AnswerCount (nullable)
* CommentCount
* FavoriteCount
* ClosedDate (present only if the post is closed)
* CommunityOwnedDate (present only if post is community wikied)